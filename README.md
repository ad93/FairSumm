# FairSumm: A fair text summarization algorithm

Code and Dataset used in the paper titled, *Summarizing User-generated Textual Content: Motivation
and Methods for Fairness in Algorithmic Summaries* at 2019 ACM Conference on Computer-Supported Cooperative Work and Social Computing (ACM CSCW).

If you are using this code or dataset for any research publication, please cite the following paper as the source of the code and dataset.

Abhisek Dash, Anurag Shandilya, Arindam Biswas, Kripabandhu Ghosh, Saptarshi Ghosh, and Abhijnan Chakraborty. "Summarizing User-generated Textual Content: Motivation and Methods for Fairness in Algorithmic Summaries”. Proceedings of the ACM on Human-Computer Interaction, ACM, vol. 3, No. CSCW, Article 172, November 2019.

BibTex:

@article{dash2019summarizing,<br/>
  title={Summarizing User-generated Textual Content: Motivation and Methods for Fairness in Algorithmic Summaries},<br/>
  author={Dash, Abhisek and Shandilya, Anurag and Biswas, Arindam and Ghosh, Kripabandhu and Ghosh, Saptarshi and Chakraborty, Abhijnan},<br/>
  journal={Proceedings of the ACM on Human-Computer Interaction},<br/>
  volume={3},<br/>
  number={CSCW},<br/>
  pages={172},<br/>
  year={2019},<br/>
  publisher={ACM}<br/>
}


### Prerequisites


	-JDk 1.7 or greater
	 
	-Python
	 -nltk
	 -pandas
	 -numpy
	 -scipy
	 
### Basic Usage

#### Example
To run *FairSumm* on *Claritin* dataset with *equal representation* fairness notion for a summary of 50 tweets, execute the following command from the project home directory:<br/>
	``python FairSumm.py --file Claritin.txt``<br/>

#### Options
You can check out the other options available to use with *FairSumm* using:<br/>
	``python FairSumm.py --help``

#### Datasets
We use three tweet datasets [*can be found in the dataset folder*] related to (a) Claritin drug side-effects, (b) MeToo movement and (c) US-presidential election to generate fair summaries. (Details can be found in the paper)

#### Input
The supported input text file format is as following:
	
	-Input file for FairSumm.py (Default settings is for equal representation fairness notion.) 
	-You need to change it as per your requirements by giving the desired number of tweets from each classes.
	
	 -input<||>input dataset
	 -length<||>length of the output summary
	 -num_groups<||>number of socially salient groups in the dataset
	 -group1<||>required number tweets in the final summary
	 -group2<||>required number tweets in the final summary
	
	-Tweets to summarize
	 -tweetId<||>tweetLabel<||>tweetText
	 
	-Similarity between tweets
	 -.csv file with similarity scores between tweets (To be generated)

Claritin.txt, METOO.txt and US-Election.txt are sample input files for generating summaries of length 50 tweets that follow the equal represenation fairness notion, from the three datasets respectively.

#### Output
The obtained summary of specified number of tweets for the dataset will get stored in the *Summaries* folder in the name of the input dataset. (Will get created)<br/>

If you set the evaluation variable to 1 then Rouge scores will be evaluated and stored as described below: <br/>
Rouge 1 and Rouge 2 Recall and F-scores will be stored in an additional file- Final\_Output.txt (will get created) in the following order (separated by tabs) in the parent directory:

	 -SummaryName	Rouge-1 Recall	Rouge-1 F-Score	Rouge-2 Recall	Rouge2- F-Score

In case you need to add more human generated summary you can add them in the Test_Summaries folder of the corresponding dataset.

### Miscellaneous

Please send any questions you might have about the code and/or the algorithm to <dash.abhi93@iitkgp.ac.in>.

*Note:* This is only a reference implementation of the *FairSumm* algorithm and could benefit from several performance enhancement schemes, some of which are discussed in the paper.



