# Packt Book Ideas

A prosocial bot can win against antisocial bots through cooperation. We can't let them divide us!

## Titles
- BYOB: Built Your Own Bot
- semantic index of the book's text within the book's text!

## Prosocial Machine Learning

### big ideas
- **prosocial == long term** metrics
    - positive sum game allowance
    - underfitting allowance
    - generalization vs stereotyping
    - user dopamine hit, vs long term quality of life
    - predicting quality of life is hard and requires assumptions about what good is
    - parents give us **good** objective functions when we are young, but move to incentivizing selfishness in societies that emphasize monetary success and individualism (big gulp cashier at a county fair)
    - egoless machine (programmer's/business's ego removed)
    - unintended consequences of short-term metrics/goals (paperclip factory AI)
- **bias variance tradeoff** irrelevant in modern bigdata world
    - false dichotomy: bias, variance, unseen new data (generalization) tradeoff
- **feature selection/engineering**:
    - feature selection bad (elbow method is black art like stock trace "technical" analysis)
    - don't ignore frequent or infrequent features based on assumptions of domain (stop words)
    - don't ignore colinear features
    - build feature selection into the model (regularization is better than feature elimination/selection)
    - deep learning is automatic feature generation
    - deep learning can't do efficient representations that involve products
    - manual feature engineering can be fun, but inefficient
    - automatic can be computationally impractical
    - back propogation and neural networks make automation practical
    - try MNIST with grid search feature engineering
    - equivalence of FE and FS
- no such thing as **unsupervised learning** (reinforcement learning, at least), you have to use the model and decide whether it's predictions or labels are helpful or hurtful, scientifically, quantitatively, with some measure of performance
- causal graphs for causal model estimation
    - occam's razor
    - account for unknown unknowns
    - Wright and model-free approach to prediction (p. 88 BoW)
    - Pearson and spurious correlation
- **hyperspace**
    - counter intuitive nature of 4+D vector algebra
    - distances
    - clustering
    - searching (ANN)
- **cross validation**
    - 2+fold CV antiquated idea only suited to scarce, expensive data with high DOF models
    - P-value irrelevant for bigdata
- **simulated toy problems** for learning
    - simulating and experimenting to understand fundamental preinciples
    - feature extraction (polynomial regression)
    - feature representation (orbital mechanics)
    - overfitting/underfitting (occam's razor)
    - good to know the **right answer** (causal model)
    - can test rules of thumb and other guesses at causal inference
- **statistical models**
    - dice rolling

## Chapters

1. what is a model (real world sports or natural world example)
2. estimating function parameters (linear regression)
3. guessing the form of the function (polynomial regression)

## AI for Healthcare (ala Stanford course textbook)

## Ideas

## Manning Corpus

- semantic index of all Manning titles
  - plagerism detection for Manning
  - editor/coaching for Manning
  - student/reader detection
  - help authors (including myself) research their topic
  - help editors source writers
  - help editors identify trends and the scope of their books and refresh rates
- style/wording suggestions/auto-complete
- grade level comparison of Manning and O'Riley and other tech publishers
- how do you encode "I love bots" sentiment into a chatbot and have it sometimes say that
  - statistical markhov chain
  - underlying physical knowlege of the world, say something then use semantics/stats to find right words/grammar

## Content

- hardware (supercomputer, GPUs, AWS GPUs, tensor flow)
- "environment" anaconda, Docker, puppet, ansible, datascience toolbox
- virtual machines
- cloud storage, AWS spot prices
- BIDMach
- Kaggle

## Build a Chatbot that helps write a book about Building a Chatbot that ...

So you want to learn about using Python for Natural Language Processing. Join me in climbing onto the shoulders of a host of giants. The deep-thinker giants I'm talking about are Jurafsky, Manning, Schutze, Norvig, and the craftsmen giants are all the awesome contributors to open source packages like NLTK, Numpy, Pandas, Scikit-Learn, Gensim, and Python itself. As we learn about these concepts and packages together we'll gradually assemble a Natural Language python to train a state-of-the-art Chatbot. I even used my chatbot to help write this book. So in a way this bot of yours can be self-aware and self-reproducing (artificially insemenated with your ideas). This may be a first. Encoding human brains with the help of a chatbot which in turn ensures the evolution and propogation of this "species" of chatbots in symbiotic, pro-social interraction with humans.

## Google search

### search: Conflating clicks with usefulness
Wired mag email 2020-10-23

Because of that, the argument goes, Google doesn’t have to worry about maintaining quality or continuing user-focused innovation in its search product. Indeed, for all the technology advances that we’ve seen in the last decade, particularly in AI, Google’s web search sometimes seems worse than it was some years ago. The famous “10 blue links”—the organic, unpaid results when you typed in a search query—are now almost buried in a Ginza-like display of ads, maps, and product recommendations. Antitrust expert Tim Wu wrote recently that Google gets away with this because it has vanquished any real competition.

Marissa Mayer, Google’s 20th employee who later went on to lead Yahoo!, once told me that for many years, Google would do a test: It would show a certain percentage of users a version of search with no ads, to see if people preferred a commercially pristine experience. The result, she boasted, was that users would consistently use the ad-supplied search engine more—they liked ads, and found them useful. When I asked Google if it still conducted this test, no one seemed to recall doing it in the first place. Which means, I guess, that they don’t do it anymore. If they did, I suspect the result might be different. (Google tells me that it does do tests in general to see if its ads are welcome, or whether they repel people.)

But if Google web search has deteriorated in quality (an assessment Google vigorously denies) that begs the question as to why competitors haven’t taken advantage. Certainly if Amazon or Facebook had created superior general interest search engines, they would have the wherewithal to pay Apple and others for placement. But after seemingly testing a run at Google, both have retreated. Amazon started a search company in the heart of Silicon Valley called A9, but it never developed a direct Google competitor. In 2013 Facebook introduced Graph Search, which seemed to have some advantages over Google search—namely, access to the social data on Facebook. But that experiment fizzled as well.
