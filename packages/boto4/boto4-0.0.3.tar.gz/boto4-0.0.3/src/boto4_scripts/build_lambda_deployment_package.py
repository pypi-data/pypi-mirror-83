import subprocess
import shlex
from typing import List, Tuple, Optional


def __run_command(argstr: str) -> int:
    return subprocess.run(shlex.split(argstr.strip(), posix=False)).returncode


def __parse_pipfile() -> List[Tuple[str, List[Tuple[str, str]]]]:
    sections: List[Tuple[str, List[Tuple[str, str]]]] = []
    with open('Pipfile') as pipfile:
        current_section: Optional[Tuple[str, List[Tuple[str, str]]]] = None
        for line in [x.strip() for x in pipfile.read().splitlines()]:
            if not any(x in line for x in ['[', '=']):
                continue
            if line.startswith('['):
                if current_section:
                    sections.append(current_section)
                current_section = (line.replace('[', '').replace(']', ''), [])
            else:
                tokens = [x.strip() for x in line.split('=')]
                tokens = [tokens[0], '='.join(tokens[1:])]
                current_section[1].append((str(tokens[0]), str(tokens[1]).replace('"', '')))
        if current_section and current_section[1]:
            sections.append(current_section)
    return sections


def main():
    parsed_pipfile = __parse_pipfile()
    __run_command('rm -rf .build')
    __run_command('mkdir .build')
    __run_command('cp -r src .build')
    with open('.build/requirements.txt', 'w+') as requirements_file:
        packages = next((x for x in parsed_pipfile if x[0] == 'packages'), (None, None))[1]
        if not packages:
            return
        for package, version in packages:
            requirements_file.write('%s%s\n' % (package, ('' if version == '*' else version)))
    install_command = 'pip install -r .build/requirements.txt -t .build --compile'
    for source in [x for x in parsed_pipfile if x[0] == 'source']:
        url = next(x[1] for x in source[1] if x[0] == 'url')
        install_command += ' --extra-index-url %s --trusted-host %s' % (
            url,
            url.split('://')[-1].split('/')[0]
        )
    __run_command(install_command)


if __name__ == '__main__':
    main()