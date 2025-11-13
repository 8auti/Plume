from app import create_app
import arrow

app = create_app()

# Me permite formatear fechas a un formato mas humano (hace 2 horas, hace 2 meses, etc)
@app.template_filter('humanize')
def humanize_date(date):
    if date is None:
        return ''
    return arrow.get(date).humanize(locale='es')

if __name__ == "__main__" :
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )