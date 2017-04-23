## WSD Project Group 666 ##
### Team members ###
* Aleksi Olavi Martikainen
* Anu Tolvanen
* Sami Mäkinen
* Rasmus Lempinen

## Final report ##

### Features implemented ###
#### Mandatory ####
All mandatory features were implemented.
Hoping for close to max points on these.

#### Optional ####
We got email validation, bootstrap(mobile friendly) working.
Game save/load feature works on some games.
3rd party login, facebook posts or RESTful API not implemented
Expecting ok points for the ones we implemented.

### Successes and failures/difficulties ###
#### Successes ####
- Everyone learned the basics (and much more) of django
- Work was divided evenly
- Group coding helped understand and tackle the problems
- All mandatory features implemented and working
- Some of the optional features implemented

#### Failures and difficulties ####
- Time was an issue as we started a bit too late
- 3rd party login was implemented but not working so we decided to leave it out
- Save/load feature doesnt work on some of the games
- Altering models caused us a lot of issues (database/cache had to be cleared)
- A lot of difficulties in the beginning with the basics of django

### Work division ###
Everyone did a bit of everything. We did most of our work coding in
group face-to-face, that's why the commits are a bit unevenly divided between
team members. We had a good team and coding was fun.

### Instructions to gameshop ###
#### Login/register ####
Front page has dummytext and links to login and register. Registration via form
and email authentication required. Currently django email backend used so
heroku version has the same link that is sent in the email to authenticate.
Registration form has selection whether user wants to be a developer.

#### Play/buy games ####
Front page after login displays all games that are in the service. Shop contains
the games user hasn't bought. Library has the games user owns. If user owns the
game the link redirects to game playing page and if not, shop view is shown.
Game page displays top 10 global highscores of the game selected.
Currently the service doesn't have a balance system so everyone can basically
purchase everything.

#### Developers ####
If user selected developer, profile contains link to dev page. The dev page
has list of the games added to the service by user. Dev page also has sales
statistics and an option to remove the game from service.

## Planned features ##
### Views ###
- Front page (introduction, links to login)
- Login page
- Register page
- Game list
- Game adding page
- Game page (Where the game is played)
- Game buying page
- Profile, nick, email, list of games owned by user
- List of games submitted by dev

### Models
##### Game
- name
- description
- url
- price
- sales (times sold)
- developer (foreignKey Developer)
- players(manytomany field Player)
- date published

##### Player
- user (foreignKey User)
- email
- nick
- (saved games) TODO

##### Developer
- user(one-to-one relation to User)

##### Highscore
- player (foreignKey Player)
- game (foreignKey Player)
- score


### Other features ###
- Authentication
- Games ( 3 own + 3rd party games )
- 3rd party login
- Email validation
- Security restrictions
- Basic game inventory and sales statistics
- Play games
- Django auth
- login, logout, register(player or dev)
- Buy games, play games, see game high scores
- high scores

### How features are implemented ###

Timeline:
1. ~~Make a skeleton for the program (project folders) /templates, /css, /images~~
2. Implement at least one javascript game per group member
3. Empty views/templates and navigation between them (urls.py, views.py, templates)
4. Create models and login functionality
5. Test models, views and login
6. Edit the views to correspond the requirements
7. Minimum required features
8. (possible additional features)

All pages will be implemented with django templates.

#### Some key features described: ####

- Login: Authentication using django authentication
- Registeration: Register with a form, (possible email validation)
- Playing games: Inside an iframe

### How we plan to work on with the project ###
- f2f meetings regularly
- Telegram for communication
- Git issues for assigning work
  * 24 open issues in Gitlab
- Google docs for project plan
