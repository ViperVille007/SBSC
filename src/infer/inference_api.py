"""
This script support LLM API inference with cot/pal/tora/sbsc prompt.
It can be used to generate tora corpus.
Code based on: https://github.com/microsoft/ProphetNet/tree/master/CRITIC
"""
import json
import random
import os
import pprint
import re
import argparse
import time
from datetime import datetime
from tqdm import tqdm
from sympy.printing.pretty import pretty

# from api.llm_api import llm_api # use your own API like OpenAI API
from utils.python_executor import PythonExecutor
from utils.utils import *
from utils.parser import *
# from utils.trajectory import *
from eval.grader import *
from utils.data_loader import load_data
from infer.inference import prepare_data


api_key = os.getenv("API_KEY")

import anthropic
client = anthropic.Anthropic(api_key=api_key)
def llm_api(engine="claude-3-5-sonnet-20240620", prompt="",demo_prompt="", max_tokens=1024, temperature=0, top_p=1.0, system="You are a math expert.", stop=None, retries=5, delay=5):
    for attempt in range(retries):
        try:
            response = client.messages.create(
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": demo_prompt + prompt},
                ],
                model=engine,
                temperature=temperature,
                top_p=top_p,
                stop_sequences=["```output"],
            )
            return [response.content[0].text]
        except Exception as e:
            print(f"Error occurred: {e}. Retrying... ({attempt + 1}/{retries})")
            time.sleep(delay)
    raise Exception("Failed to generate a response after multiple attempts.")





def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_name", default="gsm8k", type=str)
    parser.add_argument("--data_dir", default="./data", type=str)
    parser.add_argument("--model_name_or_path", default="gpt-4", type=str)
    parser.add_argument("--output_dir", default="./output", type=str)
    parser.add_argument("--prompt_type", default="tora", type=str)
    parser.add_argument("--split", default="test", type=str)
    parser.add_argument("--num_test_sample", default=-1, type=int) # -1 for full data
    parser.add_argument("--seed", default=0, type=int)
    parser.add_argument("--start", default=0, type=int)
    parser.add_argument("--end", default=-1, type=int)
    parser.add_argument("--temperature", default=0, type=float)
    parser.add_argument("--n_sampling", default=1, type=int)
    parser.add_argument("--top_p", default=1, type=float)
    parser.add_argument("--max_tokens_per_call", default=1024, type=int)
    parser.add_argument("--shuffle", action="store_true")
    parser.add_argument("--use_train_prompt_format", action="store_true")
    args = parser.parse_args()
    args.top_p = 1 if args.temperature == 0 else args.top_p # top_p must be 1 when using greedy sampling (vllm)
    return args

def add_variable_prints(code):
    lines = code.split('\n')
    processed_lines = []

    for line in lines:
        spaces = ""
        for i in line:
            if i == " ": spaces += " "
            else: break  
        if not "=" in line or line.split("=")[1].strip().isnumeric():
            processed_lines.append(line)
            continue
        variables = line.split("=")[0].strip().split(",")
        # line = spaces + "try: " + line.strip() + "\n" + spaces + "except: pass"
        processed_lines.append(line)
        for var in variables:
            var = var.strip()
            processed_lines.append(f'{spaces}try: print("{var}: ", {var})\n{spaces}except: pass')
    return '\n'.join(processed_lines)

def program_wrap(program):
    '''program = program.replace('\n', '\n    ')
    program = """\ntry:\n    from sympy import *\n    import sympy as sp\n{}\nexcept Exception as e:\n    print(e, "FAIL")\n""".format(program)
    return program'''
    prog = '''from sympy import *
import sympy as sp
from sympy import symbols
import string
# Generate a string of all lowercase and uppercase alphabets
alphabet = string.ascii_lowercase + string.ascii_uppercase
# Create symbols for all alphabets
symbols_dict = symbols(alphabet)
# If you want to have individual symbol variables, you can use exec() to define them in the local scope
for letter in alphabet:
    exec(f"{letter} = symbols('{letter}')")'''
    prog+=program
    return prog

def debug_simple(program, output, error, executor):
    debug_prompt = """You are given a program and the errors in the program along with the program output. Think step by step and debug the program. Write the entire debugged program at the end
    Program with errors:
    {}
    Errors: {}
    Outputs: {} 
    """
    prompt = debug_prompt.format(program, error, output)
    program = llm_api(prompt=prompt)[0]
    program = extract_program(program)
    wrapped = program_wrap(program)
    prediction, report = executor.apply(wrapped)
    return prediction, report

def debug_other(program, output, error, executor):
    debug_prompt = """You are given a program and the errors in the program along with the program output. Try using a non-sympy based approach and write the new code at the end.
    Program with errors:
    {}
    Errors: {}
    Outputs: {} 
    """
    prompt = debug_prompt.format(program, error, output)
    program = llm_api(prompt=prompt)[0]
    program = extract_program(program)
    wrapped = program_wrap(program)
    prediction, report = executor.apply(wrapped)
    return prediction, report

def debug_brute(program, output, error, executor):
    debug_prompt = """You are given a program and the errors in the program along with the program output. Try to replicate the same code without using sympy library and a brute force approach. You can use long loops and others for the brute force approach.
    Program with errors:
    {}
    Errors: {}
    Outputs: {}
    Brute Force approach:
    """
    prompt = debug_prompt.format(program, error, output)
    program = llm_api(prompt=prompt)[0]
    program = extract_program(program)
    wrapped = program_wrap(program)
    prediction, report = executor.apply(wrapped)
    return prediction, report

def debug_print(program, output, error, executor):
    debug_prompt = """You are given a program and the errors in the program along with the program output. Try to debug using try except block and add print statements after all the necessary places with detailed descriptions.
    Program with errors:
    {}
    Errors: {}
    Outputs: {} 
    """
    prompt = debug_prompt.format(program, error, output)
    program = llm_api(prompt=prompt)[0]
    program = extract_program(program)
    wrapped = program_wrap(program)
    pred, report = executor.apply(wrapped)
    return pred, report

def modify_print(program, output, error, executor):
    if error: error="Errors: " + error
    if output: output="Outputs: " + output
    debug_prompt = """You are given a program and the outputs and the errors of the program. Try to debug if any error is present. Now add try except blocks to each and every part of the code to prevent errors from stopping further execution. Add print statements after all the necessary places with detailed descriptions.
    Program:
    {}
    {}
    {}
    Write the whole modified code with print statements at the end.
    """
    prompt = debug_prompt.format(program, error, output)
    program = llm_api(prompt=prompt)[0]
    program = extract_program(program)
    wrapped = program_wrap(program)
    prediction, report = executor.apply(wrapped)
    return f"{error}\n```\n\n```python\n"+program+"```\n```output\n"+prediction, report

def debug(program, output, error, executor):
    prediction, report = debug_simple(program, output, error, executor)
    if "FAIL" not in prediction: return prediction, report
    # prediction, report = debug_other(program, output, error, executor)
    # if "FAIL" not in prediction: return prediction, report
    # prediction, report = debug_brute(program, output, error, executor)
    # if "FAIL" not in prediction: return prediction, report
    prediction, report = debug_print(program, output, error, executor)
    if "FAIL" not in prediction: return prediction, report
    # pred = ""
    # start = 0
    # for lines in prediction.split('\n'):
    #     if start: pred+=lines
    #     if "```" in lines: start=1
    prediction, report = modify_print(program, output, error, executor)
    return prediction, report

def execute_program(program, executor, verbose):
    #print("********Executing Program*********")
    wrapped = program_wrap(program)
    #print("***************PROGRAM STARTS HERE********\n", wrapped)
    #print("***************PROGRAM ENDS HERE********\n")
    prediction, report = executor.apply(wrapped)
    #print(prediction, report)
    # prediction += "FAIL"
    if "FAIL" in prediction:
        try:
            error = prediction.strip().split('\n')[-1][:-5]
            output = prediction.strip().split('\n')[:-1]
            output = '\n'.join(output)
            # print("ERROR: ", error)
            prediction, report = debug(program, output, error, executor)
        except Exception as e:
            prediction, report = executor.apply(wrapped)
            return prediction[:-5], report
        # print("MODIFIED: ", prediction)
    # else: prediction, report = debug(program, prediction, "", executor)
    return prediction, report

def verify_query(query, executor):
    verify_prompt = f"""You are a Math expert teacher. You are given a question and a chain of response to the question. The solution may not be complete but that is none of your task.
    Your task is to check whether the solution upto that part is correct by cross checking. For this, you need to find the outputs we have got till this part and write a single python program which checks whether the outputs we got till this part satisfy the conditions of the problem or not.
    You should write print statements in the code with description of the same.
    Query: {query}
    Verification:
    """
    answer = llm_api(prompt=verify_prompt)[0]
    program = extract_program(answer)
    wrapped = program_wrap(program)
    prediction, report = executor.apply(wrapped)
    if "FAIL" in prediction: prediction = ""
    pattern = r'<suggestions>(.*?)</suggestions>'
    # matches = re.findall(pattern, answer, re.DOTALL)
    # if matches:
    #     extracted_text = matches[0]
    #     prediction = extracted_text + prediction
    # else: pass
    return prediction

def api_with_func_call(engine,data_name,prompt_type, prompt, max_tokens, temperature, top_p, executor, max_func_call=15, verbose=False):
    '''if n > 1:
        assert temperature > 0'''

    if verbose:
        print("\n======= API with function call (START) =======")

    next_batch_queries = [""] #* n
    end_queries = []
    for i in range(max_func_call):
        # print("Call {} / {}".format(i+1, max_func_call))
        batch_outputs = []
        pred_rep = {}
        batch_queries = next_batch_queries
        if len(batch_queries) == 0:
            break
        # get all outputs
        # support batch inference when n > 1
        if data_name in ["odyssey","olympiadbench"] and prompt_type == "l2m_pal":
            data_name = "aime"
        prompt_1 = load_prompt(data_name, prompt_type) # for all other prompts with solutions       
        prompt_2 = load_prompt(data_name, prompt_type) # for all other prompts with solutions 
        if prompt_type == "l2m_pal":
            prompt_1 = load_prompt(f"{data_name}_breakdown", prompt_type) # for question breakdown in l2m
        if i == 0:
            results = llm_api(
                engine=engine, prompt=prompt + batch_queries[0], max_tokens=max_tokens, temperature=temperature,
                #n=n, 
                demo_prompt=prompt_1,
                top_p=top_p, 
                stop=["```output\n", "---"],
            )
            batch_outputs.extend(results)
        else:
            for k, query in enumerate(batch_queries):
                # print("Call {} / {}".format(k+1, len(batch_queries)))
                results = llm_api(
                    engine=engine, prompt=prompt + query, max_tokens=max_tokens, temperature=temperature,
                    #n=1, 
                    demo_prompt=prompt_2,
                    top_p=top_p, 
                    stop=["```output\n", "---"],
                )
                batch_outputs.append(results[0])

        # process all outputs
        next_batch_queries = []
        for query, output in zip(batch_queries, batch_outputs):
            #print("QUERY: ", query)
            output = output.rstrip()
            #output = output.split("```output")[0]
            #print("*******OUTPUT*******\n", output)
            query += output
            #print("*******QUERY*******\n", query)
            if verbose:
                print("\n", "-" * 100, "\n\n\n")
                print(output, end="")
                print("\n", "-" * 100, "\n\n\n")
            if "END OF CODE" in output:
                end_queries.append(query)
                break
            #if "boxed" not in output or "boxed" in output:
            #if "END OF CODE" not in output:
            if query:    
                program = extract_program(query)
                if program:
                    #print("PROGRAM FOUND!")
                    prediction, report = execute_program(program, executor, verbose)
                    #print("PREDICTION: ", prediction)
                    #print("REPORT: ",report )
                    if prediction in pred_rep: pred_rep[prediction] += 1
                    else: pred_rep[prediction] = 1
                    if pred_rep[prediction] >= 3:
                        query += "REPETITIVE ERROR"
                        end_queries.append(query)
                        continue
                    exec_result = prediction if prediction else report
                    exec_result = f"\n```output\n{exec_result.strip()}\n```\n"
                    #print("**********EXECUTION RESULT***********", exec_result)
                    #print("**********EXECUTION DONE***********")
                    query += exec_result
                    # ver_result = verify_query(query, executor)
                    # if ver_result: query += "Verification: " + ver_result
                    if verbose:
                        print(exec_result, end="")
                    if prompt_type == "l2m_pal":
                        if "boxed" in query:
                            #print('boxed occurred!!!!!!!!')
                            end_queries.append(query)
                            break
                    if "boxed" in exec_result:
                        #print('boxed occurred!!!!!!!!')
                        end_queries.append(query)
                        break
                else:
                    print("PROGRAM NOT FOUND!")
                # not end
                if i == max_func_call - 1 :
                    query += "\nEND."
                    end_queries.extend(next_batch_queries)
                next_batch_queries.append(query)
            else:
                print("END OF CODE FOUND")
                end_queries.append(query)

    end_queries.extend(next_batch_queries)
    return end_queries

import concurrent.futures
import json
from tqdm import tqdm

def process_example(args, example, executor):
    idx = example['idx']

    # parse question and answer
    example['question'] = parse_question(example, args.data_name)
    gt_cot, gt_ans = parse_ground_truth(example, args.data_name)
    full_prompt = construct_prompt(args, example)

    # call LLM, return list
    if "tora" in args.prompt_type or "sbsc" in args.prompt_type or "pal" in args.prompt_type or "l2m_pal" in args.prompt_type:
        results = api_with_func_call(
            engine=args.model_name_or_path,
            prompt=full_prompt,
            data_name=args.data_name,
            prompt_type=args.prompt_type,
            max_tokens=args.max_tokens_per_call,
            temperature=args.temperature,
            #n=args.n_sampling,
            top_p=args.top_p,
            executor=executor,
        )
    else:
        stop_tokens = ["</s>", "---", "```output"]
        #if args.prompt_type in ['cot']:
        #    stop_tokens.append("\n\n")
        results = llm_api(
            engine=args.model_name_or_path,
            prompt=full_prompt,
            demo_prompt=load_prompt(args.data_name, args.prompt_type),
            max_tokens=args.max_tokens_per_call,
            temperature=args.temperature,
            #n=args.n_sampling,
            top_p=args.top_p,
            stop=stop_tokens,
        )

    # deal with error
    if results == ['error']:
        print(f">>> Error API call for example {idx}")
        return None, None

    print(f"Get {len(results)} results for example {idx}")

    # get prediction
    predictions = []
    reports = []
    for r in results:
        pred, report = run_execute(executor, r, args.prompt_type, execute=True)
        predictions.append(pred)
        reports.append(report)

    print(f"Executed {len(predictions)} results for example {idx}")

    scores = [math_equal(p, gt_ans, timeout=True) for p in predictions]

    is_correct = scores[0]

    sample = {'idx': idx, 'question': example['question'], 'gt_cot': gt_cot, 'gt': gt_ans,
              'pred': predictions, 'score': scores}

    if args.prompt_type == "cot":
        sample.update({'code': results})
    elif "tora" in args.prompt_type or "pal" in args.prompt_type or "sbsc" in args.prompt_type or "l2m_pal" in args.prompt_type:
        sample.update({'report': reports, 'code': results})
    
    # add remaining fields
    for key in ['level', 'type', 'unit', 'solution_type', 'choices', 'solution', 'ques_type',
                'ans_type', 'answer_type', 'dataset', 'subfield', 'filed', 'theorem', 'answer']:
        if key in example:
            sample[key] = example[key]

    return sample, is_correct

def main_parallel(args):
    examples, processed_samples, out_file = prepare_data(args)
    print(out_file)
    print(len(examples))

    # init python executor
    '''if "pal" in args.prompt_type:
        executor = PythonExecutor(get_answer_expr='solution()')
    else:
        executor = PythonExecutor(get_answer_from_stdout=True)'''
    executor = PythonExecutor(get_answer_from_stdout=True)
    writer = open(out_file, 'w')
    correct, wrong = 0, 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as pool:
        futures = [
            pool.submit(process_example, args, example, executor)
            for example in examples
        ]

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            try:
                sample, is_correct = future.result()
                if sample:
                    if is_correct:
                        correct += 1
                    else:
                        wrong += 1

                    try:
                        writer.write(json.dumps(sample) + '\n')
                        writer.flush()
                    except:
                        print(">>> Error writing to file")
                        continue

                    if correct + wrong > 0:
                        print("Number of correctly solved questions: ", correct)
                        print("Total Number of questions: ", correct + wrong)
                        print("Avg Acc:", correct / (correct + wrong))
                    print()
            except Exception as e:
                print(f"Exception occurred: {e}")

    writer.close()
    print()
    if correct + wrong > 0:
        print("Avg Acc:", correct / (correct + wrong))



def main(args):
    examples, processed_samples, out_file = prepare_data(args)
    print(out_file)
    print(len(examples))
    # init python executor
    '''if "pal" in args.prompt_type:
        executor = PythonExecutor(get_answer_expr='solution()')
    else:
        executor = PythonExecutor(get_answer_from_stdout=True)'''
    executor = PythonExecutor(get_answer_from_stdout=True)

    writer = open(out_file, 'w')
    correct, wrong = 0, 0

    for example in tqdm(examples, total=len(examples)):
        idx = example['idx']

        # parse question and answer
        example['question'] = parse_question(example, args.data_name)
        gt_cot, gt_ans = parse_ground_truth(example, args.data_name)
        full_prompt = construct_prompt_l2m(args, example)
        # print(full_prompt)

        # call LLM, return list
        if "tora" in args.prompt_type or "sbsc" in args.prompt_type or "pal" in args.prompt_type or "l2m_pal" in args.prompt_type:
            results = api_with_func_call(
                engine=args.model_name_or_path,
                prompt=full_prompt,
                data_name=args.data_name,
                prompt_type=args.prompt_type,
                max_tokens=args.max_tokens_per_call,
                temperature=args.temperature,
                #n=args.n_sampling,
                top_p=args.top_p,
                executor=executor,
            )
        else:
            stop_tokens = ["</s>", "---", "```output"]
            #if args.prompt_type in ['cot']:
            #    stop_tokens.append("\n\n")
            results = llm_api(
                engine=args.model_name_or_path,
                prompt=full_prompt,
                max_tokens=args.max_tokens_per_call,
                demo_prompt=load_prompt(args.data_name, args.prompt_type),
                temperature=args.temperature,
                #n=args.n_sampling,
                top_p=args.top_p,
                stop=stop_tokens,
            )
        # deal with error
        if results == ['error']:
            print(">>> Error API call")
            continue
        print("Get {} results".format(len(results)))
        # get prediction
        predictions = []
        reports = []
        for r in results:
            pred, report = run_execute(executor, r, args.prompt_type, execute=True)
            predictions.append(pred)
            reports.append(report)
        print("Executed {} results".format(len(predictions)))
        
        scores = [math_equal(p, gt_ans, timeout=True) for p in predictions]

        is_correct = scores[0]
        if is_correct:
            correct += 1
        else:
            wrong += 1

        sample = {'idx': idx, 'question': example['question'], 'gt_cot': gt_cot, 'gt': gt_ans,
            'pred': predictions, 'score': scores}

        if args.prompt_type == "cot":
            sample.update({'code': results})
        elif "tora" in args.prompt_type or "pal" in args.prompt_type or "sbsc" in args.prompt_type:
            sample.update({'report': reports, 'code': results})
        # add remain fields
        for key in ['level', 'type', 'unit', 'solution_type', 'choices', 'solution', 'ques_type', \
            'ans_type', 'answer_type', 'dataset', 'subfield', 'filed', 'theorem', 'answer']:
            if key in example:
                sample[key] = example[key]

        # print(idx)
        # show_sample(sample)
        if correct + wrong > 0:
            print("Avg Acc:", correct / (correct + wrong))
        print()
    
        try:
            writer.write(json.dumps(sample) + '\n')
            writer.flush()
        except:
            print(">>> Error writing to file")
            continue

    writer.close()
    print()
    if correct + wrong > 0:
        print("Avg Acc:", correct / (correct + wrong))


if __name__ == "__main__":
    args = parse_args()
    set_seed(args.seed)
    main_parallel(args)
    #main(args)
