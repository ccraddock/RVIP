
# Rapid Visual Information Processing (RVIP) Task

R. Cameron Craddock<sup>1,2,†</sup>

<sup>1</sup>Nathan S. Kline Institute for Psychiatric Research, Orangeburg, NY, <sup>2</sup>Child Mind Institute, New York, NY

<sup>†</sup>Contact [cameron.craddock@childmind.org](mailto:cameron.craddock@childmind.org) with any comments or questions.

## Task Description

This is a [PsychoPy](http://www.psychopy.org/) (Peirce, 2008) implementation of the rapid visual information processing (RVIP) task described in [Wesnes and Warburton, 1983](http://www.ncbi.nlm.nih.gov/pubmed/6425892) and is similar to the [implementation](http://www.cambridgecognition.com/tests/rapid-visual-information-processing-rvp) provided with Cambridge Cognition's [CANTAB](http://www.cambridgecognition.com/) cognitive battery (Sahakian and Owen, 1992).

The RVIP assesses working memory and sustained attention. Neuroimaging experiments using PET have found that this task activates a bilateral fronto-parietal network (Coull et al., 1996). Response times and detection accuracy from this task have been previously correlated with DMN function (Pagnoni, 2012). 

![Fig. 1 Example stimuli for RVIP task.](rvip_stim.png?raw=true "Fig. 1 Example stimuli for RVIP task.")

A pseudo-random stream of digits (0-9) is presented to the participants in white, centered on a black background, surrounded by a white box (see Fig 1). Participants are instructed to press the space bar whenever they observe the sequences 2-4-6, 3-5-7, or 4-6-8. Digits are presented one after another at a rate of 100 digits per minute and the number of stimuli that occurred between targets varied between 8 and 30. Responses that occurred within 1.5 seconds of the last digit of a target sequence being presented were considered “hits”. Stimuli presentation continued until a total of 32 target sequences were encountered, which required on average 4 minutes and 20 seconds. Before performing the task, participants completed a practice version that indicated when a target sequence had occurred and provided feedback (“hit” or “false alarm”) whenever the participant pressed the space bar. Participants were allowed to repeat the practice until they felt that they were comfortable with the instructions.

## Example Performance

Results from 125 participants (21-45 years old, with a variety of clinical and subclinical psychiatric symptoms)  from the openly shared [Enhanced Nathan Kline Institute - Rockland Sample Neurofeedback study](http://fcon_1000.projects.nitrc.org/indi/enhanced/) are illustrated in figure 2.

![Fig. 2 illustrates the hit rate, false alarm rate, and A' for 125 particpants from the Enhanced Nathan Kline Institute - Rockland Sample Neurofeedback study](rvip_performance.png?raw=true "Fig. 2 illustrates the hit rate, false alarm rate, and A' for 125 particpants from the Enhanced Nathan Kline Institute - Rockland Sample Neurofeedback study.")


## Usage Notes

This task requires that the [PsychoPy](http://www.psychopy.org/) ecosystem be installed either as python libraries, or as a standalone application (available for Mac OSX and Microsoft Windows). For Debian systems (including Ubuntu), PsychoPy can be easily installed via [NeuroDebian](http://neuro.debian.net/pkgs/psychopy.html?highlight=psychopy).

The task uses the keyboard space bar for participant input. Once started, the task will ask the user to input a participant ID, which will be used for naming the output files, and to indicate whether training should be performed. The task will create a Data/ directory in the current directory to store participant responses. Responses will be stored in a file whose name includes the participant ID entered by the user and the data and time the task was started.

The task stimuli are not randomly generated, this proved to be too hard. Instead the included ```stim_sep_gen.py``` script is used to generate a list of inter-stimulus intervals between targets. This sequence is permuted prior to each run and then used to generate the stimuli.

This task is NOT designed to work with fMRI and would need to be optimized for event related design before doing so.

## Scoring Responses

Summary statistics calculated from the RVIP included: mean reaction time, total targets, hits, misses, false alarms, hit rate (H), false alarm rate (F), and A’ (Eqn. 1, A’ is an alternative to the more common d’ in signal detection theory (Stanislaw and Todorov, 1999)). These are automatically calculated by the task script and are written to the log file at the end of the task. 

Responses that occur within 1.5 seconds of the last digit of a target sequence being displayed are considered hits, multiple responses within 1.5 seconds are considered a hit followed by multiple false alarms, and responses that occur outside of the 1.5-second window are considered false alarms. The number of hits and false alarms are converted to rates by dividing by the total number of targets. Since the number of false alarms are not bounded, the false alarm rate can be higher than 100%, resulting in A’ values greater than 1

These scores can be recalculated from the logfiles generated by the task.

## Acknowledgements
Salary support was provided by NIMH BRAINS R01MH101555 to RCC.

## References

Coull, J. T., Frith, C. D., Frackowiak, R. S. J., & Grasby, P. M. (1996). A fronto-parietal network for rapid visual information processing: a PET study of sustained attention and working memory. Neuropsychologia, 34(11), 1085–1095. [http://doi.org/10.1016/0028-3932(96)00029-2](http://doi.org/10.1016/0028-3932(96)00029-2)

Pagnoni, G. (2012). Dynamical Properties of BOLD Activity from the Ventral Posteromedial Cortex Associated with Meditation and Attentional Skills. J Neurosci, 32(15), 5242–5249. Journal Article. [http://doi.org/10.1523/JNEUROSCI.4135-11.2012](http://doi.org/10.1523/JNEUROSCI.4135-11.2012)

Peirce, J. W. (2008). Generating Stimuli for Neuroscience Using PsychoPy. Frontiers in Neuroinformatics, 2, 10. [http://doi.org/10.3389/neuro.11.010.2008](http://doi.org/10.3389/neuro.11.010.2008)

Sahakian, B. J., & Owen, A. M. (1992). Computerized assessment in neuropsychiatry using CANTAB: discussion paper. Journal of the Royal Society of Medicine, 85(7), 399–402. Retrieved from [http://www.ncbi.nlm.nih.gov/pubmed/1629849](http://www.ncbi.nlm.nih.gov/pubmed/1629849)

Wesnes, K., & Warburton, D. M. (1983). Effects of smoking on rapid information processing performance. Neuropsychobiology, 9(4), 223–229. [http://doi.org/10.1159/000117969](http://doi.org/10.1159/000117969)


