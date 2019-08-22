# FairSumm: A fair text summarization algorithm

Code and Dataset used in the paper titled, Summarizing User-generated Textual Content: Motivation
and Methods for Fairness in Algorithmic Summaries at 2019 ACM Conference on Computer-Supported Cooperative Work and Social Computing (ACM CSCW).

If you are using this code or dataset for any research publication, or for preparing a technical report, you must cite the following paper as the source of the code and dataset.

Abhisek Dash, Anurag Shandilya, Arindam Biswas, Kripabandhu Ghosh, Saptarshi Ghosh, and Abhijnan Chakraborty. "Summarizing User-generated Textual Content: Motivation and Methods for Fairness in Algorithmic Summaries”. In Proceedings of the 2019 ACM Conference on Computer-Supported Cooperative Work and Social Computing (ACM CSCW), Austin, Texas, November 2019.

BibTex:

@inproceedings{dash2016summarizing,
title={Summarizing User-generated Textual Content: Motivation and Methods for Fairness in Algorithmic Summaries},
author={Dash, Abhisek and Shandilya, Anurag and Biswas, Arindam and Ghosh, Kripabandhu and Ghosh, Saptarshi and Chakraborty, Abhijnan},
booktitle={Computer-Supported Cooperative Work and Social Computing (ACM CSCW), 2019 ACM Conference on},
year={2019},
organization={ACM}
}


### Prerequisites

*JDK 1.7 or greater

*Python modules
*nltk
*pandas
*numpy
*scipy

### Basic Usage

#### Example
To run *FairSumm* on Claritin dataset with equal representation fairness notion for a summary of 50 tweets, execute the following command from the project home directory:<br/>
	``python FairSumm.py --input Claritin --notion equal --length 50``

#### Options
You can check out the other options available to use with *FairSumm* using:<br/>
	``python FairSumm.py --help``

#### Input
The supported input text file format is as following:
	-Tweets
	 -tweet id<||>tweet label<||>tweet text
	 
	-Similarity between tweets
	 -.csv file with similarity scores between tweets

#### Output
The output file is a summary of *length* number of tweets stored in the *Summaries* folder. 

### Miscellaneous

Please send any questions you might have about the code and/or the algorithm to <dash.abhi93@iitkgp.ac.in>.

*Note:* This is only a reference implementation of the *FairSumm* algorithm and could benefit from several performance enhancement schemes, some of which are discussed in the paper.

