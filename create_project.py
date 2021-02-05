import os
import sys
from time import sleep
import base64
from CustomArgParse import CustomArgParse
from selenium import webdriver

PROJECTS_PATH = r"Python_Projects"
DRIVER_PATH = r"chromedriver.exe"
USERNAME = "github username"
PASSWORD = "github password"


def create_new_project(project_name):
    if os.path.isdir(PROJECTS_PATH):
        full_path_project = os.path.join(PROJECTS_PATH, project_name)
        try:
            pass
            os.mkdir(full_path_project)
        except FileExistsError:
            sys.exit(f"The project name specified already exists: '{project_name}'")
        except FileNotFoundError:
            sys.exit(f"The project name specified is not valid: '{project_name}'")
    else:
        raise ValueError(f"{PROJECTS_PATH} is not a valid directory path!")
    # call git_setup function
    git_setup(full_path_project, project_name)


def git_setup(project_directory, project_name):
    # change the working directory to the project directory
    os.chdir(project_directory)
    os.system("git --version")
    os.system("git init")
    git_project_path = create_github_project(project_name)
    os.system(f"git remote add origin {git_project_path}")
    with open('.gitignore', 'w') as f:
        f.write("\n".join(["venv", ".idea"]))


def create_github_project(project_name):
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get('https://github.com/login')
    # user_name
    driver.find_element_by_xpath('//*[@id="login_field"]').send_keys(USERNAME)
    # user_pass
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(base64.b64decode(PASSWORD).decode('utf-8'))
    # sign_in
    driver.find_element_by_xpath('//*[@id="login"]/div[4]/form/input[14]').click()
    driver.get('https://github.com/new')
    # repository_name
    driver.find_element_by_xpath('//*[@id="repository_name"]').send_keys(project_name)
    # check_readme_file
    driver.find_element_by_xpath('//*[@id="repository_auto_init"]').click()
    # create_repo
    sleep(0.5)
    driver.find_element_by_xpath('/html/body/div[4]/main/div/form/div[4]/button').click()
    sleep(1)
    driver.find_element_by_xpath(
        '//*[@id="repo-content-pjax-container"]/div[2]/div[1]/div[2]/span/get-repo/details/summary').click()
    git_project_path = driver.find_element_by_xpath(
        '//*[@id="repo-content-pjax-container"]/div[2]/div[1]/div[2]/span/get-repo/details/div/div/'
        'div[1]/div/tab-container/div[2]/div/input').get_attribute('aria-label')
    driver.quit()
    return git_project_path


if __name__ == "__main__":
    args_dict = {'project': ['p', ' Name of the Project to be created']}
    arg = CustomArgParse(args_dict)
    new_project_name = arg.get_args()['project']
    create_new_project(new_project_name)



