# hudsonsystem
Player management and scoring. Using similar ideas to that of an elo or glicko rating system.
Run main.py
Click the drop down and select "Competitors"
Use up/down arrow keys to scroll through the list.
Hit enter while the highlight is on "New" then fill in the details.
The first column is the id which every player has to have a different one.
The second is their name or any other nametype.
The third is teamtype1 and fourth teamtype2.
You can change the name of these in the settings. 
By default they are set to, "UUID", "Name", "House", "Grade"
You can also change the dafualt starting value for players in the settings

To change the elo/rating/score of the players, hit the drop down in the top left corner, then click "Enter Scores"
Then type the UUID into the box, hit enter, then type in the next players UUID
Then click either, "Player A Won", "Draw", or "Player B Won".
Once clicked, an adjusted elo will be shown under their name.
These changes are not saved until you hit "Submit"

After you have entered the results of a few games you can go to the drop down and click "Competitors"
Now you can see the names of the players and their scores.
