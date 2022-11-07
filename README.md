CS 50 AI
A10 Traffic

Experimentation process:

Once I had the load_data function up and running I started my experimentation baselining my model from the ‘handwriting’ lecture example and working with the gtsrb-small dataset. Making small changes, one at a time, first concentrating on the convolution layer instruction (number or filters, kernel size) to view the effects on the output stats. However I found that working with the small dataset gave me mostly very similar stats. So I felt I needed to start working with the larger dataset.

In the beginning I was mostly focused on trying different kernel sizes, Although after a few tests I found that increasing my kernel size did not necessarily produce a more accurate model. Then I came across an article (https://towardsdatascience.com/deciding-optimal-filter-size-for-cnns-d6f7b56f9363) which helped explain why my kernel will probably be most effective and efficient if I keep it small and have odd number dimensions. So I decided to stick with a 3x3 kernel!

I then shifted my focus to experimenting with the Dense layer(s). One of the first things I noticed was that changing my dense layer number of units by small amounts, didn’t make any significant difference. While researching more about dense layers I came across this stack overflow QA: (https://stackoverflow.com/questions/57387485/how-to-choose-units-for-dense-in-tensorflow-keras) which suggested using steps/increments while tuning your model, for example (8, 16, 32 ,64, 128…). My original thought was that I should start by using dense layer(s) with large number of units. I tested all kinds of dense layer configuration combinations of 1-3 dense layers with different combinations of units, number of dropouts with different dropout rates… I was running shell scripts overnight queueing up traffic.py with added parameters to set all these combinations… And after a couple of nights, my conclusion was that past a certain number of dense layer units I wasn’t gaining any significant accuracy but the algorithm was beginning to take much longer. Finally, having a few dense layers with a proportionally smaller amount of units was more effective than a single dense layer. Also, having too much dropout was obviously no good but having too little dropout caused the model to overfit. Finally, I settled on using 2 dense layers with units in reverse steps (16, 8) each multiplied by the number of categories. I feel this model produces very respectable accuracy and loss figures while completing execution in a reasonable amount of time on my machine. Unfortunately I had to go over the 5 minute video length limit to do this, my video is ~9 min, I hope this is still OK.

Thank you for the great learning module!