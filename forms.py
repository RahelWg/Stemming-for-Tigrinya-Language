from flask_wtf import *
from wtforms import *
from wtforms.validators import DataRequired ,Length

class  StemmingForm(FlaskForm):
     characters= StringField('Characters',
                            validators=[DataRequired(), Length(max= 50000 )])

     stem=SubmitField('Stem')
