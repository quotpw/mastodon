# Import the necessary packages
from consolemenu import *
from consolemenu.items import *
from handlers import constants

# Create the menu
menu = ConsoleMenu("Mastodon", "Multitool for mastodon social network (analogue of twitter)")

function_item = FunctionItem("Call a Python function", input)
for function in constants.handlers:
    menu.append_item(FunctionItem(function, constants.handlers[function]))

# Finally, we call show to show the menu and allow the user to interact
menu.show()
