# -*- coding: utf-8 -*-

import re

import inquirer


class Example:
    def text(self):
        questions = [
            inquirer.Text(
                "name",
                message="What's your name",
            ),
            inquirer.Text(
                "surname",
                message="What's your surname",
            ),
            inquirer.Text(
                "phone",
                message="What's your phone number",
                validate=lambda _, x: re.match("\+?\d[\d ]+\d", x),
            ),
        ]
        answers = inquirer.prompt(questions)
        print(answers)

    def editor(self):
        questions = [inquirer.Editor("long_text", message="Provide long text")]
        answers = inquirer.prompt(questions)
        print(answers)

    def list(self):
        questions = [
            inquirer.List(
                "size",
                message="What size do you need?",
                choices=["Jumbo", "Large", "Standard", "Medium", "Small", "Micro"],
            ),
        ]
        answers = inquirer.prompt(questions)
        print(answers)

    def checkbox(self):
        questions = [
            inquirer.Checkbox(
                "interests",
                message="What are you interested in?",
                choices=[
                    "Computers",
                    "Books",
                    "Science",
                    "Nature",
                    "Fantasy",
                    "History",
                ],
            ),
        ]
        answers = inquirer.prompt(questions)
        print(answers)

    def path(self):
        questions = [
            inquirer.Path(
                "log_file",
                message="Where logs should be located?",
                path_type=inquirer.Path.DIRECTORY,
            ),
        ]
        answers = inquirer.prompt(questions)
        print(answers)


example = Example()
# example.text()
# example.editor()
# example.list()
# example.checkbox()
# example.path()
