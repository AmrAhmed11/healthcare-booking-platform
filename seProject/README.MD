# SE_PROJECT

### Environment setup
1) `pip install pipenv`
2) `pipenv shell`
3) `pip install -r requirements.txt`

#### before push
` pip freeze > requirements.txt`

#### after pull
` pip install -r requirements.txt `

#### at the end 
` pkill -f runserver `