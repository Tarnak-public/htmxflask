def create_select_option(known_faces_list):
    options_values = ""
    for j in range(len(known_faces_list)):
        options_values += '<option value="' + str(j) + '">' + known_faces_list[j] + '"</option>'

    return options_values
