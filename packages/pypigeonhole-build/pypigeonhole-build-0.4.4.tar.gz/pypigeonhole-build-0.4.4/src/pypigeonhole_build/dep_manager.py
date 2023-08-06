import pypigeonhole_build.pip_translator as pip_translator
import pypigeonhole_build.conda_translator as conda_translator
from pypigeonhole_build.conda_translator import CONDA


def main(args, dependent_libs):
    if len(args) < 2:
        raise ValueError('need to pass in parameters: pip, conda, conda_env, etc')
    # scripts use these
    if args[1] == 'pip':
        pip_translator.gen_req_txt(dependent_libs, 'requirements.txt')
    elif args[1] == 'conda':
        conda_translator.gen_conda_yaml(dependent_libs, 'environment.yml')
    elif args[1] == 'conda_env':
        print(CONDA.env)
    else:
        raise ValueError(f'unknown parameter {args[1]}')
