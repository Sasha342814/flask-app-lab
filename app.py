from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    # Форма-заглушка: реальної відправки немає
    return render_template('contacts.html', title='Контакти')


if __name__ == '__main__':
    app.run(debug=True)
