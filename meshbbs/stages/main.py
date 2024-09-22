import meshbbs.stages
import meshbbs.stages.about
import meshbbs.stages.help

stages = [
    meshbbs.stages.about,
    meshbbs.stages.help
]



main_message = "Welcome to Meshtastic BBS\n"

for i in stages:
    main_message = main_message + f"[{i.letter}] {i.name}\n"

def get_option(message: str):
    return_function = main_menu

    for i in stages:
        if message.lower() == i.letter.lower():
            (next_stage, return_string) = i.run_stage()
            if next_stage == None:
                next_stage = main_menu
                return_string = return_string + "\n" + main_message
            return (next_stage, return_string)

    return(get_option, "Unknown option\n\n" + main_message)
        
def main_menu(message: str = None):
    return_string = main_message

    next_stage = get_option
    return (next_stage, return_string)