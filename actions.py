def build_message(form):
    first_name = form['firstName']
    last_name = form['lastName']
    return f'Salut, {first_name} {last_name}! Apasa aici pentru a-ti confirma email-ul!'
