from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from usvisa.pipeline.prediction_pipeline import USvisaData, USvisaClassifier

app = Flask(__name__)
CORS(app) 

class DataForm:
    def __init__(self, form):
        self.continent = form.get("continent")
        self.education_of_employee = form.get("education_of_employee")
        self.has_job_experience = form.get("has_job_experience")
        self.requires_job_training = form.get("requires_job_training")
        self.no_of_employees = form.get("no_of_employees")
        self.company_age = form.get("company_age")
        self.region_of_employment = form.get("region_of_employment")
        self.prevailing_wage = form.get("prevailing_wage")
        self.unit_of_wage = form.get("unit_of_wage")
        self.full_time_position = form.get("full_time_position")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            form = DataForm(request.form)
            usvisa_data = USvisaData(
                continent=form.continent,
                education_of_employee=form.education_of_employee,
                has_job_experience=form.has_job_experience,
                requires_job_training=form.requires_job_training,
                no_of_employees=form.no_of_employees,
                company_age=form.company_age,
                region_of_employment=form.region_of_employment,
                prevailing_wage=form.prevailing_wage,
                unit_of_wage=form.unit_of_wage,
                full_time_position=form.full_time_position,
            )

            usvisa_df = usvisa_data.get_usvisa_input_data_frame()
            model_predictor = USvisaClassifier()
            value = model_predictor.predict(dataframe=usvisa_df)[0]
            status = "Visa-approved" if value == 1 else "Visa Not-Approved"

            return render_template("usvisa.html", context=status)

        except Exception as e:
            return jsonify({"status": False, "error": str(e)}), 400

    return render_template("usvisa.html", context="Rendering")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
