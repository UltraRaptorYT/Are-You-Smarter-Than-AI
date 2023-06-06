from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired


class PredictionForm(FlaskForm):
    cough = RadioField(
        'cough', choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()])
    muscle_aches = RadioField(
        "muscle_aches", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    tiredness = RadioField(
        "tiredness", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    sore_throat = RadioField(
        "sore_throat", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    runny_nose = RadioField(
        "runny_nose", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    stuffy_nose = RadioField(
        "stuffy_nose", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    fever = RadioField(
        "fever", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    nausea = RadioField(
        "nausea", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    vomiting = RadioField(
        "vomiting", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    diarrhea = RadioField(
        "diarrhea", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    shortness_of_breath = RadioField(
        "shortness_of_breath", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    difficulty_breathing = RadioField(
        "difficulty_breathing", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    loss_of_taste = RadioField(
        "loss_of_taste", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    loss_of_smell = RadioField(
        "loss_of_smell", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    itchy_nose = RadioField(
        "itchy_nose", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    itchy_eyes = RadioField(
        "itchy_eyes", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    itchy_mouth = RadioField(
        "itchy_mouth", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    itchy_inner_ear = RadioField(
        "itchy_inner_ear", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    sneezing = RadioField(
        "sneezing", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    pink_eye = RadioField(
        "pink_eye", choices=[('1', 'True'), ('0', 'False')], validators=[InputRequired()]
    )
    submit = SubmitField("Submit")
