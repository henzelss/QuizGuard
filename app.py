from website import create_app
#wrap the program in socket io

app = create_app()

# only if we run this file not when we import our file
if __name__ == '__main__':
    app.run(debug=True) 


# Model- View - Presenter 
# Model: The data and the logic that manipulates the data. In Flask, this typically refers to the database or other data storage mechanism.
# View: The presentation layer that handles user interaction and displays the data to the user. In Flask, this typically refers to the HTML templates that are rendered by the web server and sent to the user's browser.
# Presenter: The intermediary component that connects the model and view components. It processes the user input, retrieves the data from the model, and passes it on to the view for display.
# student view all the quiz