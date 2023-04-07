import re

def generate_prompt(prompt, histories, ctx=None):
    print("----inside")

    ctx = "" if ctx is None or ctx == "" else f"""
    
    Context:{ctx
    
    }"""

    convs = f"""Di seguito è riportata una cronologia delle istruzioni che descrivono le attività, abbinate a un input che fornisce ulteriore contesto. Scrivi una risposta che completi adeguatamente la richiesta ricordando la cronologia della conversazione.
{ctx}
"""

    for history in histories:
        history_prompt = history[0]
        history_response = history[1]

        history_response = history_response.replace("<br>", "\n")

        pattern = re.compile(r'<.*?>')
        history_response = re.sub(pattern, '', history_response)        

        convs = convs + f"""### Istruzione:{history_prompt}

### Risposta:{history_response}

"""

    convs = convs + f"""### Istruzione:{prompt}

### Risposta:"""

    print(convs)
    return convs

def post_process(bot_response):
    bot_response = bot_response.split("### Risposta:")[-1].strip()
    bot_response = bot_response.replace("\n", "<br>")     # .replace(" ", "&nbsp;")
    
    pattern = r"(  )"
    replacement = r'<span class="chat_wrap_space">  <span>'
    return re.sub(pattern, replacement, bot_response)

def post_processes(bot_responses):
    return [post_process(r) for r in bot_responses]
