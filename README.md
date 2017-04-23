## WSD Project Group 666 ##
### Team members ###
* Aleksi Olavi Martikainen
* Anu Tolvanen
* Sami Mäkinen
* Rasmus Lempinen

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
