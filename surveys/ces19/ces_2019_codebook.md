       Canadian Election Study 2019
         Online Survey Codebook
                                     Version 1.0

                                    April 29, 2020


All use of the 2019 Canadian Election Study data must be appropriately referenced and
credited. The correct citation is: Stephenson, Laura B., Allison Harell, Daniel Rubenson
and Peter John Loewen. The 2019 Canadian Election Study – Phone Survey. [dataset].




                                                                                       0
      1. Contents
2.     Summary of the CES2019 online survey data....................................................................... 5
3.     Suggested citation ................................................................................................................. 6
4.     Acknowledgements ............................................................................................................... 7
5.     Sample design and survey weights ....................................................................................... 8
     5.1     Sample design................................................................................................................ 8
       5.1.1        Campaign Period Survey (CPS) ............................................................................. 8
       5.1.2        Post-Election Survey (PES) .................................................................................... 9
     5.2     Panels ............................................................................................................................ 9
     5.3     Survey weights ............................................................................................................. 10
6.     Data Quality ......................................................................................................................... 10
     6.1     Campaign Period Survey ............................................................................................. 11
       6.1.1        Removal criteria .................................................................................................... 11
       6.1.2        Identification of duplicates ..................................................................................... 12
       6.1.3        Table of data quality .............................................................................................. 12
     6.2     Post-Election Survey .................................................................................................... 14
       6.2.1        Matching Respondents to Campaign Period Survey ............................................ 14
       6.2.2        Removal criteria .................................................................................................... 14
       6.2.3        Identification of duplicates ..................................................................................... 15
       6.2.4        Table of data quality .............................................................................................. 15
7.     Survey design ...................................................................................................................... 17
     7.1     Required responses ..................................................................................................... 17
     7.2     Auto-advance ............................................................................................................... 17
     7.3     Variable naming ........................................................................................................... 18
     7.4     Additional question modules ........................................................................................ 18
8.     Campaign Period Survey..................................................................................................... 20
     8.1     Metadata ...................................................................................................................... 20
     8.2     Survey flow ................................................................................................................... 25
     8.3     Questions ..................................................................................................................... 36
       8.3.1        Consent and quota demographics ........................................................................ 36
       8.3.2        Democracy, voting, and parties............................................................................. 63
       8.3.3        Ideology ............................................................................................................... 108
       8.3.4        Leader impressions ............................................................................................. 112


                                                                                                                                                1
       8.3.5       Government spending ......................................................................................... 120
       8.3.6       Issue positions .................................................................................................... 124
       8.3.7       The economy ...................................................................................................... 134
       8.3.8       Party issue handling ............................................................................................ 137
       8.3.9       Party chances ..................................................................................................... 139
       8.3.10      Election outcomes ............................................................................................... 143
       8.3.11      Immigration and refugees ................................................................................... 146
       8.3.12      Efficacy ................................................................................................................ 148
       8.3.13      Election promises ................................................................................................ 152
       8.3.14      SNC-Lavalin affair ............................................................................................... 153
       8.3.15      News consumption .............................................................................................. 155
       8.3.16      Political participation ........................................................................................... 157
       8.3.17      Duty to vote ......................................................................................................... 157
       8.3.18      Quebec sovereignty ............................................................................................ 158
       8.3.19      Personal finances................................................................................................ 160
       8.3.20      Political knowledge .............................................................................................. 160
       8.3.21      Premier satisfaction ............................................................................................. 164
       8.3.22      Party identification and membership ................................................................... 165
       8.3.23      Groups thermometers ......................................................................................... 182
       8.3.24      Past vote ............................................................................................................. 185
       8.3.25      Debates ............................................................................................................... 189
       8.3.26      Additional demographics ..................................................................................... 191
9.     Post Election Survey ......................................................................................................... 261
     9.1     Metadata .................................................................................................................... 261
     9.2     Survey flow ................................................................................................................. 267
     9.3     Questions ................................................................................................................... 280
       9.3.1       Consent and basic demographics ....................................................................... 280
       9.3.2       Main issue of campaign ...................................................................................... 290
       9.3.3       Voting: turnout ..................................................................................................... 291
       9.3.4       Voting: reasons and method ............................................................................... 293
       9.3.5       Voting: vote choice .............................................................................................. 298
       9.3.6       Satisfaction with democracy................................................................................ 303
       9.3.7       Attention to campaign ......................................................................................... 304


                                                                                                                                              2
9.3.8    Party contact ....................................................................................................... 304
9.3.9    Mandate .............................................................................................................. 307
9.3.10   Government formation ........................................................................................ 308
9.3.11   Party promises .................................................................................................... 310
9.3.12   Group thermometers ........................................................................................... 311
9.3.13   Party words ......................................................................................................... 312
9.3.14   Economy ............................................................................................................. 315
9.3.15   Electoral reform ................................................................................................... 316
9.3.16   Paid medical treatment ....................................................................................... 318
9.3.17   Senate ................................................................................................................. 320
9.3.18   Environment versus jobs ..................................................................................... 321
9.3.19   Democratic values ............................................................................................... 323
9.3.20   Efficacy ................................................................................................................ 326
9.3.21   Politician lies, bilingualism, and equal rights ....................................................... 329
9.3.22   Group identity ...................................................................................................... 332
9.3.23   Assimilation and immigrants taking jobs ............................................................. 334
9.3.24   Government effectiveness and programs ........................................................... 337
9.3.25   Ties with US and China and country thermometers............................................ 340
9.3.26   Comparative Study of Electoral Systems (Module 5) questions ......................... 344
9.3.27   Module questions ................................................................................................ 354
9.3.28   Interest in politics ................................................................................................ 385
9.3.29   Social networks ................................................................................................... 386
9.3.30   Participation ........................................................................................................ 393
9.3.31   Voluntary associations ........................................................................................ 403
9.3.32   Party membership in lifetime ............................................................................... 406
9.3.33   Importance of voting ............................................................................................ 406
9.3.34   Media statments .................................................................................................. 409
9.3.35   Representation by women .................................................................................. 413
9.3.36   Corruption ........................................................................................................... 414
9.3.37   Populism ............................................................................................................. 415
9.3.38   Nativism .............................................................................................................. 423
9.3.39   Canadian identification ........................................................................................ 428
9.3.40   Social Dominance Orientation............................................................................. 431


                                                                                                                                    3
9.3.41   How much should be done for <group> .............................................................. 436
9.3.42   Taxes .................................................................................................................. 440
9.3.43   Abortion ............................................................................................................... 442
9.3.44   International trade ............................................................................................... 448
9.3.45   Private sector and jobs........................................................................................ 449
9.3.46   Role of government in inequality ......................................................................... 450
9.3.47   Deservingness .................................................................................................... 450
9.3.48   Get ahead & Govt should .................................................................................... 452
9.3.49   Trust .................................................................................................................... 454
9.3.50   Inequality ............................................................................................................. 455
9.3.51   Stronger Federal or Provincial government ........................................................ 457
9.3.52   Sexism ................................................................................................................ 459
9.3.53   Climate Change .................................................................................................. 465
9.3.54   Party identification ............................................................................................... 466
9.3.55   Affective party identification ................................................................................ 474
9.3.56   Quebec questions ............................................................................................... 477
9.3.57   New lifestyles ...................................................................................................... 481
9.3.58   Life satisfaction ................................................................................................... 483
9.3.59   Cognition ............................................................................................................. 486
9.3.60   Gender identity .................................................................................................... 487
9.3.61   Big 5 .................................................................................................................... 489
9.3.62   Health initial ......................................................................................................... 492
9.3.63   Health follow-ups ................................................................................................. 493
9.3.64   Additional demographics ..................................................................................... 495




                                                                                                                                     4
  2. Summary of the CES2019 online survey data
Title                         Canada Election Study 2019
Mode                          Online survey
Population                    Canadian citizens and permanent residents,
                              aged 18 or older
Field Periods                 Campaign Period Survey: September 13th to
                              October 21st, 2019


                              Post-election survey: October 24th to
                              November 11th, 2019
Number of interviews          Pre-election survey: 37,822
                              Post-election survey: 10,337
Number of variables           620
Languages                     English and French
Weights                       Weight variables are provided; weights must
                              be used to ensure that the data is
                              representative of the population. See section
                              5.3 for more details.
Software                      The CES2019 data is provided in .dta format
                              but can be used with a variety of software
                              programs such as STATA, SPSS, R




                                                                              5
   3. Suggested citation
Stephenson, Laura B., Allison Harell, Daniel Rubenson and Peter John Loewen. The 2019
Canadian Election Study – Online Collection. [dataset]




                                                                                        6
   4. Acknowledgements
The survey sampling, programming, and weighting were performed by, or under the supervision
of, Laura Stephenson, Allison Harell, Peter Loewen and Daniel Rubenson. They are professors
of political science at the University of Western Ontario, l’Université de Québec à Montréal, the
University of Toronto and Ryerson University, respectively. Benjamin Allen Stevens, Joanie
Bouchard, Laura French, and Katherine Sullivan assisted them in this task.

The 2019 Canadian Election Study was funded by grants provided by the Social Sciences and
Humanities Research Council of Canada.




                                                                                                7
   5. Sample design and survey weights

   5.1 Sample design

The online sample for the 2019 Canadian Election Study was composed of a two-wave panel
with a modified rolling-cross section during the campaign period and a post-election recontact
wave.

   5.1.1      Campaign Period Survey (CPS)

We procured an online sample of 37,822 members of the Canadian general population through
Qualtrics, with targets stratified by region and balanced on gender and age within each region.
We aimed for 50% men and 50% women. We aimed to have 28% of our respondents aged 18-
34, 33% aged 35-54 and 39% aged 55 and higher. The regions were: Atlantic (Newfoundland
and Labrador, New Brunswick, Nova Scotia, Prince Edward Island), Quebec, Ontario Prairies
(Manitoba, Saskatchewan, Alberta), and British Columbia. Within each of those regions, the
provincial quotas were split evenly. We also aimed to have 80% French and 20% English within
Quebec, 10% French within the Atlantic region, and 10% French nationally. Respondents
needed to be aged 18 or over, and Canadian citizens or permanent residents in order to
participate.

We initially aimed for a daily sample of 1000 respondents per day for the campaign period. This
was not always achieved. We increased our targets during the last five days of the campaign, to
try to increase the total number of respondents.




                                                                                                 8
Sampling for the Campaign Period Survey occurred from September 13th to October 21st 1,
2019. The survey instrument was presented on the Qualtrics online platform.

      5.1.2       Post-Election Survey (PES)

10,340 respondents from the Campaign Period Survey were re-contacted after the election for a
follow-up survey.2 Sampling for the Post-Election Survey occurred from October 24th to
November 11th, 2019. The survey instrument was presented on the Qualtrics online platform.


      5.2 Panels

Qualtrics drew from a number of panels to construct the sample for the Campaign Period
Survey. These panels were only identified to us by the embedded data field that contained the
respondent’s panel ID. A breakdown of the number of respondents from each panel in the
cleaned data is listed below.




1
    The survey was closed at 9:00am on October 21st.
2
    We had aimed for 50% return to sample, but Qualtrics was unable to meet that target.


                                                                                                9
The metadata variables cps19_panel and pes19_panel show which panel respondents
were part of.

              Panel                Campaign Period Survey             Post-Election Survey
              PID                            12,148                           5,960
             cintid                           279                               -
               gid                           1,063                            429
                id                            942                               -
             ppsid                            201                               -
                 r                           3,203                            1956
               rid                           4,311                             776
               uig                            254                               27
               vid                            232                              123
              viga                           10,137                           1069
      No panel ID identified                  5052                              -
 Total across panels                         37,822                          10,340



   5.3 Survey weights

Weights have been created for the dataset using an iterative "raking'' process, as provided by
the ipfraking command in STATA15. Marginal values were successively weighted according to
province, as well as gender, age group, and education level. All population data were taken
from the 2016 Canadian census. A maximum of 200 iterations were completed. The dataset
includes the weights produced as 4 variables, depending on which portion of the sample is
being used:

   1. cps19_weight_general_all - all campaign period respondents
   2. cps19_weight_general_restricted - only high-quality campaign period respondents
      (see Data Quality section below)
   3. pes19_weight_general_all - all post-election survey respondents
   4. pes19_weight_general_restricted - only high-quality post-election survey respondents

Note that respondents from the territories do not have weights, as they were not included in the
sampling frame, because data collection in the territories is too sparse to be representative.



   6. Data Quality
Incomplete responses, duplicate responses of previous respondents, speeders, those who
“straight-lined” grid questions (“straightliners”), and respondents whose postal code didn’t match
their province have all been removed from the data file, and are excluded from numbers
reported in this codebook.




                                                                                               10
A small portion of the remaining respondents have been flagged by less-severe data quality
checks, but as these responses may still be useful they have been kept in the data. These were
“inattentive” respondents, who took more than 60 minutes to complete the survey, and “initial
duplicate” respondents, which means they took the survey again later, but that this was their
initial response. These respondents are identified by the variables cps19_inattentive,
cps19_duplicates_flag, pes19_inattentive, and pes19_duplicates_flag.

If these respondents are excluded, 33,905 Campaign Period Survey and 9544 Post-Election
Survey responses remain.

   6.1 Campaign Period Survey

   6.1.1       Removal criteria

During the data cleaning process, respondents were categorized based on their most important
reason for removal. While respondents might be removed for multiple reasons, the most
important reason is most relevant.

Reasons for removal, in order of importance:

   1.  Internal survey testing or previews
   2.  Ineligible - did not consent to survey
   3.  Ineligible - not a Canadian citizen or permanent resident
   4.  Ineligible - respondent under 18 years of age
   5.  Over quota
   6.  Incomplete - did not complete initial quota demographics
   7.  Incomplete - did not complete core survey
   8.  Duplicate of a previous respondent (identified by IP address and the following
       demographics: year of birth, gender, education level, employment, religion, immigration
       status)
   9. Speeder (completed the survey in less than 500 seconds, or 8.3 minutes)
   10. Postal code-province mismatch
   11. Straightliner

The following values are in the final dataset

   12. Inattentive
   13. Initial duplicate (identified by IP address and demographics, took survey again later)
   14. Completed the core survey, but not the modules
   0. Clean complete




                                                                                                11
      6.1.2       Identification of duplicates

Duplicate responses to the survey (that is, the same respondent taking a survey multiple times)
were identified using the following values. A response was flagged as a duplicate if they had the
same values as another response to the survey for each of the following demographics
responses, or had the same panel ID.

              Values used to identify duplicate responses in the Campaign Period Survey
                      Value                                          Variable name
                   IP address3                                              -
                   Year of birth                                       cps19_yob
                     Gender                                          cps19_gender
                    Education                                      cps19_education
                   Employment                                      cps19_employment
                     Religion                                       cps19_religion
                 Immigration status                              cps19_bornin_canada

Of the responses flagged as duplicates, the first response was kept in the dataset (and flagged
with the variable cps19_duplicates_flag, as they are still useful, while subsequent
responses were removed.

      6.1.3       Table of data quality

Once the cleaning was complete, we ended up with 37,822 responses, of which 33,905 were
high quality and 3,917 were slightly lower quality.


            cps19_data_quality |      Freq.     Percent        Cum.
-------------------------------+-----------------------------------
                Clean complete |     33,905       45.48       45.48
       Internal survey testing |        220        0.30       45.78
       Ineligible - no consent |      8,051       10.80       56.58
Ineligible - not citizen or PR |      1,073        1.44       58.02
         Ineligible - under 18 |        188        0.25       58.27
                    Over quota |      9,470       12.70       70.97
 Incomplete quota demographics |      4,865        6.53       77.50
               Incomplete core |      5,569        7.47       84.97
          Subsequent duplicate |      2,309        3.10       88.07
                       Speeder |      1,490        2.00       90.07
  Postalcode-province mismatch |         55        0.07       90.14
                 Straightliner |      3,434        4.61       94.75
                   Inattentive |      1,789        2.40       97.15

3
    Not included in dataset, to maintain respondent anonymity.


                                                                                              12
             Initial duplicate |      1,512        2.03       99.17
            Incomplete modules |        616        0.83      100.00
-------------------------------+-----------------------------------
                         Total |     74,546      100.00




                                                                      13
   6.2 Post-Election Survey

   6.2.1       Matching Respondents to Campaign Period Survey

We matched Post Election Survey responses to their Campaign Period Survey responses by
using respondent’s panel IDs. We were unable to match some respondents using these
variables (which are not included in this dataset, as they might be personally identifiable).
Qualtrics was able to match most of the remaining respondents through other means, and those
matches have been incorporated.

We were able to use some limited demographic information to match some additional
respondents (IP address, year of birth, and province), but because few demographic variables
were repeated across the CPS and PES, those matches were not kept in the data.

   6.2.2       Removal criteria

The Post-Election Survey data cleaning followed the Campaign Period Survey, with the
following changes:

   1. There were no quotas for the PES, so that category doesn’t exist
   2. Qualtrics set the termination exit links to not save screened-out responses, so we can't
      know how many respondents did not consent, or were otherwise ineligible for the CES
      PES
   3. We did not receive matching information for respondents who did not complete the PES,
      so any respondents who completed most of the survey, but not all of it, were caught up
      in the “could not match” category.
This results in the following categories:

Removed from dataset:

   1. Internal survey testing
   2. Ineligible - under 18
   3. Incomplete quota demographics
   4. Incomplete core
   5. Subsequent duplicate
   6. Speeder
   7. Postal code-province mismatch
   8. Straightliner
   9. Could not match to CPS response
   10. Key demographics did not match CPS
   11. Matched using IP address, year of birth, and province

The following values are in the final dataset:


                                                                                            14
      12. Inattentive
      13. Initial duplicate
      14. Incomplete modules
      15. Only matched by Qualtrics, not using panel IDs
      0. Clean complete



      6.2.3       Identification of duplicates

Duplicate responses to the survey (that is, the same respondent taking a survey multiple times)
were identified using the following values. A response was flagged as a duplicate if they had the
same values as another response to the survey for each of the following demographics
responses, or had the same panel ID.

Due to the limited demographic variables available in the Post-Election Survey, the variables
used here were different than those used for the Campaign Period Survey.

                Values used to identify duplicate responses in the Post Election Survey
                         Value                                        Variable name
                      IP address4                                            -
                        Province                                    pes19_province
                  Citizenship status                                 pes19_citizen
                          Age                                          pes19_age
                    Month of birth                               pes19_month_of_birth

Of the responses flagged as duplicates, the first response was kept in the dataset (and flagged
with the variable pes19_duplicates_flag) as they are still useful, while subsequent
responses were removed.

      6.2.4       Table of data quality

Once all of the cleaning has been done, we end up with 10,340 responses, of which 8,313 were
high quality and 2,027 were medium-quality.


                     pes19_data_quality |      Freq.     Percent        Cum.
----------------------------------------+-----------------------------------
                         Clean complete |      8,313       61.62       61.62
                Internal survey testing |          3        0.02       61.64
                  Ineligible - under 18 |         21        0.16       61.80
          Incomplete quota demographics |        660        4.89       66.69

4
    Not included in dataset, to maintain respondent anonymity.


                                                                                                15
                        Incomplete core |        585        4.34       71.03
                   Subsequent duplicate |        611        4.53       75.55
                                Speeder |        151        1.12       76.67
           Postalcode-province mismatch |         15        0.11       76.78
                          Straightliner |        395        2.93       79.71
        Could not match to CPS response |        357        2.65       82.36
     Key demographics did not match CPS |         60        0.44       82.80
Only matched using IP address, YOB, and |        293        2.17       84.98
                            Inattentive |        571        4.23       89.21
                      Initial duplicate |        225        1.67       90.88
                     Incomplete modules |          3        0.02       90.90
              Only matched by Qualtrics |      1,228        9.10      100.00
----------------------------------------+-----------------------------------
                                  Total |     13,491      100.00




                                                                           16
   7. Survey design

   7.1 Required responses

One of the design requirements for the 2019 CES questionnaires was that respondents had to
be able to refuse to answer any given question (except for those used by the survey quotas or
to identify the respondent’s riding, such as province of residence). In order to comply with that
requirement while still retaining high data quality, the questionnaires made extensive use of
"Don't know/ Prefer not to answer" options, where possible, and required respondents to
respond in some way (even if only to select "Don't know/ Prefer not to answer"), except where
otherwise noted (this was primarily non-categorical questions such as sliders). For example,
some questions had the text "If you do not know, or prefer not to answer, please click →" at the
end of them. For those questions, if the respondent did not respond to that question or a
component of that question (for example, did not click on or move a slider), then their response
to that question, or that component of the question, was recorded as missing.


   7.2 Auto-advance




                                                                                               17
Auto-advance was used throughout the survey, using the survey-wide options of the Qualtrics
platform. As the survey used one question per page where possible, this meant that once
respondents had finished answering each question, they would be automatically moved to the
next page. Auto-advance did not apply to open-text questions, multiple-selection questions,
slider questions, or single-response questions when an item with a supplemental text field was
selected.5

The “back” button, represented by “←”, was available for respondents to go back to a previous
question if they wished to change their answer. However, due to platform constraints, it is not
possible to go back to a previous block. Due to the complex design of the survey, many small
blocks of questions were used, making this a common restriction.


    7.3 Variable naming

We have used descriptive names for variables, where possible, within character limits.

To help differentiate variables from the different waves of the 2019 CES, and to differentiate
between variables from different years should one combine this dataset with others, we use the
“cps19_” prefix for questions in the Campaign Period Survey, and the “pes19_” prefix for
variables in the Post-Election Survey, where possible.

Metadata variables do not usually use these prefixes, except in cases where the same variable
was used in both the Campaign Period Survey and the Post-Election Survey.


    7.4 Additional question modules

The CES2019 Campaign Period Survey, and to a lesser extent the Post-Election Survey,
included a number of additional question modules, which some respondents received. These
question modules were placed after the main survey, after the “additional demographics” block
of questions.

Respondents were allocated to up to a certain number of minutes of modules. This number was
fine-tuned over the course of the campaign period, to balance the resulting overall length of the
survey and the number of respondents required to answer the question modules. Some
question modules that included experiments on specific topics were exclusive of other modules
on similar topics. Some modules had specific sampling requirements.

The question modules were displayed in a randomized order (except for a few which had a part
1 and part 2 that required some spacing between them).


5
 More information is available on Qualtrics’ website, under the “Autoadvance” heading:
https://www.qualtrics.com/support/survey-platform/survey-module/look-feel/fonts-and-
colors/#Autoadvance


                                                                                               18
These question modules are not included in the dataset nor discussed further in the codebook.
These modules may be released by individual researchers and can be merged with this data by
matching on cps19_ResponseID.




                                                                                           19
   8. Campaign Period Survey

   8.1 Metadata

cps19_StartDate
Start timestamp for the Campaign Period Survey response, in Stata time format

cps19_EndDate
End timestamp for the Campaign Period Survey response, in Stata time format

cps19_ResponseId
Unique identification code of the Campaign Period Survey response. Mainly useful for data
management, such as combining different versions of the dataset.

cps19_current_date
Date the Campaign Period Survey response started, in YYYYMMDD format, as a number.
For example, “20191020” would be October 20, 2019.

cps19_current_date_string
Date the Campaign Period Survey response started, in YYYYMMDD format, as a string.
For example, “20191020” would be October 20, 2019.

cps19_Q_Language
Language the respondent answered the Campaign Period Survey in. “EN” is English, “FR-CA”
is French.

cps19_Q_TotalDuration
How long the respondent spent in the Campaign Period Survey, in seconds. This includes all
time from when the survey is opened, to when the response is submitted, including time spent
away from the survey, and if the respondent closes the survey and returns to it later.

get_news

Randomized embedded data field containing a flag indicating whether the respondent would
receive the question cps19_news_cons. 1 = respondent received cps19_news_cons, 0 =
they did not.

get_more_naming
Randomized embedded data field containing a flag indicating whether the respondent would
receive the questions cps19_govgen_name and cps19_presrus_name. 1 = respondent
received cps19_govgen_name and cps19_presrus_name, 0 = they did not.

get_not_vote_for


                                                                                            20
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question cps19_not_vote_for if they were otherwise eligible for it. 1 =
respondent received cps19_not_vote_for if they were otherwise eligible for it, 0 = they did
not.

get_party_issue_handling

Randomized embedded data field containing a flag indicating whether the respondent would
receive the question cps19_issue_handle. 1 = respondent received
cps19_issue_handle, 0 = they did not.

get_imp_loc_iss

Randomized embedded data field containing a flag indicating whether the respondent would
receive the question cps19_imp_loc_iss. 1 = respondent received cps19_imp_loc_iss, 0
= they did not.

get_outcome

Randomized embedded data field containing a flag indicating whether the respondent would
receive the question cps19_outcome_most and cps19_outcome_least. 1 = respondent
received cps19_outcome_most and cps19_outcome_least, 0 = they did not.

justice_law
justice_law_fr

These embedded data fields were used in a wording experiment, in which justice_law
 (which was piped into ${e://Field/justice_law}) was randomly set to be either “crime
and justice” in English (“la criminalité et la justice” in French) or “police and law enforcement”
(“la police et les forces de l’ordre” in French) for the question cps19_spend_just_law.

lr_scale_order

Respondents were randomly assigned to receive either cps19_lr_scale_bef or
cps19_lr_scale_aft, as part of an experiment on ordering effects. If the embedded data
field lr_scale_order was equal to "individual_first", they received the individual self-
placement question cps19_lr_scale_bef, and then the party placement question
cps19_lr_parties. If the embedded data field lr_scale_order was equal to
"party_first", they received the party placement question cps19_lr_parties, and then the
individual self-placement question cps19_lr_scale_aft.




                                                                                                     21
ethnicity_intro
ethnicity_intro_fr

The introductory text to cps19_ethnicity varied based on whether the respondent was a
Canadian citizen or permanent resident. For citizens, ${e://Field/ethnicity_intro} read “In addition
to being Canadian, to what ethnic or cultural group(s) do you belong?”, and for permanent
residents it read “To what ethnic or cultural group(s) do you belong?”. In the French translation,
${e://Field/ethnicity_intro_fr} contained equivalent text, “En plus d'être Canadien, à quel groupe
ethnique ou culturel appartenez-vous?” or “À quel groupe ethnique ou culturel appartenez-
vous?”.

premier
province_fr

These embedded data fields contained province-specific text, used in the question
cps19_prov_gov_sat, which required different French grammar for some provinces.

        cps19_province                     premier                        province_fr
 Alberta                             Jason Kenney              de l'Alberta
 British Columbia                    John Horgan               de la Colombie Britannique
 Manitoba                            Brian Pallister           du Manitoba
 New Brunswick                       Blaine Higgs              du Nouveau-Brunswick
 Newfoundland and Labrador           Dwight Ball               de Terre-Neuve-et-Labrador
 Northwest Territories*              Bob McLeod                des Territoires du Nord-Ouest
 Nova Scotia                         Stephen McNeil            de la Nouvelle-Écosse
 Nunavut*                            Joe Savikataaq            du Nunavut
 Ontario                             Doug Ford                 de l'Ontario
 Prince Edward Island                Dennis King               de l'Ile-du-Prince-Édouard
 Quebec                              François Legault          du Québec
 Saskatchewan                        Scott Moe                 de la Saskatchewan
 Yukon                               Sandy Silver              du Yukon
* Respondents from the territories were not intentionally sampled, but were not screened out
from the survey, so there are a small number in the data.


pid_en
pid_party_en
pid_party_fr

These embedded data fields contained federal party-specific text, based on their identification
with political parties in cps19_fed_id, used in the question cps19_fed_id_str.

    cps19_fed_id          pid_en                   pid_party_en             pid_party_fr



                                                                                                  22
 Liberal                 Liberal                 Liberal Party            Parti libéral
 Conservative            Conservative            Conservative Party       Parti conservateur
 NDP                     NDP                     NDP                      NPD
 Bloc Québécois          Bloc Québécois          Bloc Québécois           Bloc Québécois
 Green                   Green                   Green Party              Parti vert
 People’s Party          People's Party          People's Party           Parti populaire

cps19_data_quality

This embedded data field contains the most important data quality category that the respondent
is in, and was used during data review and cleaning. See section 6.1.1 for more details.

cps19_panel
Which panel the respondent was drawn from, measured during the Campaign Period Survey.

cps19_age
Respondent age in years, recoded based on their year of birth, cps19_yob.

cps19_duplicates_flag
Indicator for respondents that took the Campaign Period Survey multiple times. 0 = Unique, 1 =
Initial response of someone who took the survey again. Any subsequent responses have
already been removed from the data.

cps19_inattentive
Indicator that respondent took more than 60 minutes to complete the Campaign Period Survey.
1 = Inattentive.

constituencynumber
Number of the federal electoral district (constituency) the respondent resides in, determined
using their postal code and the Postal Code Conversion File Plus (PCCF+) available through
Statistics Canada. The constituencies of 1.5% of respondents could not be determined from the
postal code that they entered.

constituencyname
Name of the federal electoral district (constituency) the respondent resides in, determined using
their postal code and the Postal Code Conversion File Plus (PCCF+) available through
Statistics Canada. The constituencies of 1.5% of respondents could not be determined from the
postal code that they entered.

cps19_fsa
The first three digits of the respondent’s postal code from the Campaign Period Survey, also
known as their Forward Sortation Area. This can be provided upon request for research
purposes..



                                                                                               23
cps19_weight_general_all
Sample weight for all Campaign Period Survey respondents. See section 5.3 for more details.

cps19_weight_general_restricted
Sample weight for Campaign Period Survey respondents, excluding subsequent duplicates and
inattentive respondents. See section 5.3 for more details.




                                                                                              24
   8.2 Survey flow
EmbeddedData
  current_date = ${date://CurrentDate/Y}${date://CurrentDate/m}${date://CurrentDate/d}
  Q_LanguageValue will be set from Panel or URL.
  Q_TotalDurationValue will be set from Panel or URL.
EmbeddedData
  testingValue will be set from Panel or URL.
  UserAgentValue will be set from Panel or URL.
EmbeddedData
  regional_demonymValue will be set from Panel or URL.
  regional_demonym_FRValue will be set from Panel or URL.
EmbeddedData
  modulesAllocatedValue will be set from Panel or URL.
  additionalModulesLengthValue will be set from Panel or URL.
  unconstrainedChecksValue will be set from Panel or URL.

BlockRandomizer: 1 -

   EmbeddedData
     get_news = 0
   EmbeddedData
     get_news = 1

BlockRandomizer: 1 -

   EmbeddedData
     get_more_naming = 0
   EmbeddedData
     get_more_naming = 1

BlockRandomizer: 1 -

   EmbeddedData
     get_not_vote_for = 0
   EmbeddedData
     get_not_vote_for = 1

BlockRandomizer: 1 -

   EmbeddedData
     get_party_issue_handling = 0
   EmbeddedData
     get_party_issue_handling = 1

BlockRandomizer: 1 -

   EmbeddedData


                                                                                    25
      get_imp_loc_iss = 0
    EmbeddedData
      get_imp_loc_iss = 1

BlockRandomizer: 1 -

    EmbeddedData
      get_outcome = 0
    EmbeddedData
      get_outcome = 1

BlockRandomizer: 1 -

    EmbeddedData
      justice_law = crime and justice
    EmbeddedData
      justice_law = police and law enforcement

Branch: New Branch
   If
       If justice_law Is Equal to crime and justice

    EmbeddedData
      justice_law_fr = la criminalité et la justice

Branch: New Branch
   If
       If justice_law Is Equal to police and law enforcement

    EmbeddedData
      justice_law_fr = la police et les forces de l’ordre

BlockRandomizer: 1 -

    EmbeddedData
      lr_scale_order = individual_first
    EmbeddedData
      lr_scale_order = party_first

Block: Consent and quota demographics (18 Questions)

Branch: New Branch
    If
       If Letter of Information and Consent Project Title: Canadian Election Study
2019Principal Investigat... I consent to participate in this study. I have read all of the
information about the study. Is Not Selected

    EmbeddedData
      term = noconsent


                                                                                             26
       gc = 2

   EndSurvey: Advanced

Branch: New Branch
      If
          If To make sure we are talking to a cross section of Canadians, we need to get a
little information... 2002 Is Selected
          Or To make sure we are talking to a cross section of Canadians, we need to get a
little information... 2003 Is Selected
          Or To make sure we are talking to a cross section of Canadians, we need to get a
little information... 2004 Is Selected
          Or To make sure we are talking to a cross section of Canadians, we need to get a
little information... 2005 Is Selected
          Or To make sure we are talking to a cross section of Canadians, we need to get a
little information... 2006 Is Selected
          Or To make sure we are talking to a cross section of Canadians, we need to get a
little information... 2007 Is Selected
          Or To make sure we are talking to a cross section of Canadians, we need to get a
little information... 2008 Is Selected
          Or To make sure we are talking to a cross section of Canadians, we need to get a
little information... 2009 Is Selected
          Or To make sure we are talking to a cross section of Canadians, we need to get a
little information... 2010 Is Selected
          Or How old are you? 17 Is Selected

   EmbeddedData
     term = underage
     gc = 2

   EndSurvey: Advanced

Branch: New Branch
   If
       If Are you a... Other Is Selected

   EmbeddedData
     term = noncitizen_or_pr
     gc = 2

   EndSurvey: Advanced

Branch: New Branch
   If
       If Are you a... Canadian citizen Is Selected

   EmbeddedData


                                                                                        27
       ethnicity_intro = In addition to being Canadian, to what ethnic or cultural group(s)
   do you belong?
       ethnicity_intro_fr = En plus d'être Canadien, à quel groupe ethnique ou culturel
   appartenez-vous?

Branch: New Branch
   If
       If Are you a... Permanent resident Is Selected

   EmbeddedData
     ethnicity_intro = To what ethnic or cultural group(s) do you belong?
     ethnicity_intro_fr = À quel groupe ethnique ou culturel appartenez-vous?

Branch: New Branch
   If
       If Which province or territory are you currently living in? Alberta Is Selected

   EmbeddedData
     premier = Jason Kenney
     Region = West
     province_fr = de l'Alberta

Branch: New Branch
    If
       If Which province or territory are you currently living in? British Columbia Is
Selected

   EmbeddedData
     premier = John Horgan
     Region = West
     province_fr = de la Colombie Britannique

Branch: New Branch
   If
       If Which province or territory are you currently living in? Manitoba Is Selected

   EmbeddedData
     premier = Brian Pallister
     Region = West
     province_fr = du Manitoba

Branch: New Branch
    If
       If Which province or territory are you currently living in? New Brunswick Is
Selected

   EmbeddedData



                                                                                          28
       premier = Blaine Higgs
       Region = Atlantic
       province_fr = du Nouveau-Brunswick

Branch: New Branch
   If
       If Which province or territory are you currently living in? Newfoundland and
Labrador Is Selected

   EmbeddedData
     premier = Dwight Ball
     Region = Atlantic
     province_fr = de Terre-Neuve-et-Labrador

Branch: New Branch
    If
       If Which province or territory are you currently living in? Northwest Territories Is
Selected

   EmbeddedData
     premier = Bob McLeod
     Region = Territories
     province_fr = des Territoires du Nord-Ouest

Branch: New Branch
   If
       If Which province or territory are you currently living in? Nova Scotia Is Selected

   EmbeddedData
     premier = Stephen McNeil
     Region = Atlantic
     province_fr = de la Nouvelle-Écosse

Branch: New Branch
   If
       If Which province or territory are you currently living in? Nunavut Is Selected

   EmbeddedData
     premier = Joe Savikataaq
     Region = Territories
     province_fr = du Nunavut

Branch: New Branch
   If
       If Which province or territory are you currently living in? Ontario Is Selected

   EmbeddedData



                                                                                         29
       premier = Doug Ford
       Region = Ontario
       province_fr = de l'Ontario

Branch: New Branch
    If
       If Which province or territory are you currently living in? Prince Edward Island Is
Selected

   EmbeddedData
     premier = Dennis King
     Region = Atlantic
     province_fr = de l'Ile-du-Prince-Édouard

Branch: New Branch
   If
       If Which province or territory are you currently living in? Quebec Is Selected

   EmbeddedData
     premier = François Legault
     Region = Quebec
     province_fr = du Québec

Branch: New Branch
    If
       If Which province or territory are you currently living in? Saskatchewan Is
Selected

   EmbeddedData
     premier = Scott Moe
     Region = West
     province_fr = de la Saskatchewan

Branch: New Branch
   If
       If Which province or territory are you currently living in? Yukon Is Selected

   EmbeddedData
     premier = Sandy Silver
     Region = Territories
     province_fr = du Yukon

EmbeddedData
  Region2 = National
EmbeddedData
  Age_Score = ${gr://SC_d5nYDFNuR9TAjxr/Score}




                                                                                        30
Branch: New Branch
   If
       If Age_Score Is Equal to 1

   EmbeddedData
     Age = 18-34

Branch: New Branch
   If
       If Age_Score Is Equal to 2

   EmbeddedData
     Age = 35-54

Branch: New Branch
   If
       If Age_Score Is Equal to 3

   EmbeddedData
     Age = 55+

Standard: Democracy, voting, and parties (46 Questions)
Standard: Ideology - left-right scales (6 Questions)
Standard: Leader impressions (8 Questions)

BlockRandomizer: 5 -

   Standard: Government spending - education (2 Questions)
   Standard: Government spending - environment (2 Questions)
   Standard: Government spending - justice_law (2 Questions)
   Standard: Government spending - defence (2 Questions)
   Standard: Government spending - immigrants and minorities (2 Questions)

Standard: Issue positions - intro (2 Questions)

BlockRandomizer: 3 -

   Standard: Issue positions - electoral reform (2 Questions)
   Standard: Issue positions - assisted dying (2 Questions)
   Standard: Issue positions - cannabis (2 Questions)
   Standard: Issue positions - carbon tax (2 Questions)
   Standard: Issue positions - pipelines (2 Questions)
   Standard: Issue positions - environmental regulation (2 Questions)
   Standard: Issue positions - environment versus jobs (2 Questions)
   Standard: Issue positions - subsidies (2 Questions)
   Standard: Issue positions - free trade (2 Questions)

Standard: The economy (6 Questions)


                                                                             31
Branch: New Branch
   If
       If get_party_issue_handling Is Equal to 1

   Standard: Party issue handling (2 Questions)

Standard: Party chances (4 Questions)

Branch: New Branch
   If
       If get_outcome Is Equal to 1

   Standard: Election outcome (4 Questions)

BlockRandomizer: 2 -

   Standard: Immigration (2 Questions)
   Standard: Refugees (2 Questions)

Standard: Efficacy intro (2 Questions)

BlockRandomizer: 3 -

   Standard: Efficacy - understand (2 Questions)
   Standard: Efficacy - say in government (2 Questions)
   Standard: Efficacy - politician ethics (2 Questions)

Standard: Trudeau election promises (2 Questions)
Standard: SNC (2 Questions)

Branch: New Branch
   If
       If get_news Is Equal to 1

   Standard: News consumption (2 Questions)

Standard: Political participation (2 Questions)
Standard: Duty to vote (2 Questions)

Branch: New Branch
   If
       If Which province or territory are you currently living in? Quebec Is Selected

   Standard: Quebec sovereignty (2 Questions)

Standard: Personal finances (2 Questions)
Standard: Political knowledge (8 Questions)
Standard: Premier satisfaction (2 Questions)
Standard: Party ID and membership part 1 (2 Questions)



                                                                                        32
Branch: New Branch
   If
       If In federal politics, do you usually think of yourself as a: Liberal Is Selected

    EmbeddedData
      pid_en = Liberal
    EmbeddedData
      pid_party_en = Liberal Party
    EmbeddedData
      pid_party_fr = Parti libéral

Branch: New Branch
    If
       If In federal politics, do you usually think of yourself as a: Conservative Is
Selected

    EmbeddedData
      pid_en = Conservative
    EmbeddedData
      pid_party_en = Conservative Party
    EmbeddedData
      pid_party_fr = Parti conservateur

Branch: New Branch
   If
       If In federal politics, do you usually think of yourself as a: NDP Is Selected

    EmbeddedData
      pid_en = NDP
    EmbeddedData
      pid_party_en = NDP
    EmbeddedData
      pid_party_fr = NPD

Branch: New Branch
    If
       If In federal politics, do you usually think of yourself as a: Bloc Québécois Is
Selected

    EmbeddedData
      pid_en = Bloc Québécois
    EmbeddedData
      pid_party_en = Bloc Québécois
    EmbeddedData
      pid_party_fr = Bloc québécois




                                                                                            33
Branch: New Branch
   If
       If In federal politics, do you usually think of yourself as a: Green Is Selected

    EmbeddedData
      pid_en = Green
    EmbeddedData
      pid_party_en = Green Party
    EmbeddedData
      pid_party_fr = Parti vert

Branch: New Branch
    If
       If In federal politics, do you usually think of yourself as a: People’s Party Is
Selected

    EmbeddedData
      pid_en = People's Party
    EmbeddedData
      pid_party_en = People's Party
    EmbeddedData
      pid_party_fr = Parti populaire

Standard: Party ID and membership part 2 (14 Questions)
Standard: Groups thermometers (2 Questions)
Standard: Past vote (6 Questions)
Standard: Debates (4 Questions)
Standard: Additional demographics (34 Questions)

Branch: New Branch
   If
       If Q_TotalDuration Is Less Than 500

    EmbeddedData
      term = Speeder
      gc = 4

    EndSurvey: Advanced

Branch: New Branch
   If
       If Q_TotalDuration Is Greater Than or Equal to 3600

    EmbeddedData
      term = Inattentive
      gc = 4



                                                                                          34
   EndSurvey: Advanced

EmbeddedData
  gc = 1

EndSurvey: Advanced
Page Break




                         35
   8.3 Questions

   8.3.1       Consent and quota demographics


Start of Block: Consent and quota demographics




cps19_consent

Letter of Information and Consent
 Project Title: Canadian Election Study 2019
 Principal Investigator: Laura Stephenson, PhD, Political Science, University of Western
Ontario, (519) 661-2111 x85164, laura.stephenson@uwo.ca
 Co-Investigators: Allison Harell, PhD, Political Science, Université de Québec à Montréal,
(514) 987-3000 x5676, harell.allison@uqam.ca
 Peter Loewen, PhD, Political Science, Munk School of Global Affairs, University of Toronto,
(416) 978-5120, peter.loewen@utoronto.ca
 Daniel Rubenson, PhD, Politics and Public Administration, Ryerson University, (416) 979-5000
x4052, rubenson@ryerson.ca

 Thank you for considering taking our survey. You can complete the survey in English or in
French. Please choose your preferred language using the drop-down menu at the top right of
this screen (vous pouvez choisir de compléter ce sondage en français ou en anglais en
sélectionnant la langue de votre choix à l’aide du menu déroulant situé dans le coin supérieur
droit de l'écran).

We are doing a research study about Canadians' attitudes about current events, elections and
democracy, and we would like your opinions. Participation in the research is voluntary. Your
answers will be kept completely confidential and will be used for research purposes only. You
must be 18 years or older and a legal resident of Canada to participate.

 Today’s survey will take about 20 minutes to complete. If you participate today you may be re-
contacted at a later date and invited to complete additional surveys as well. Participation in any
additional surveys will also be voluntary.

 To read additional information and details about this study, including your rights as a research
participant, how you will be compensated for your time and how your data will be stored, please
click HERE. If you would like to complete the survey, please click the appropriate link below.




                                                                                                 36
If you have questions at any time about the study or its results, you may contact:
Dr. Laura Stephenson
Department of Political Science
University of Western Ontario
London, Ontario, Canada
1-519-661-2111 ext. 85164
Laura.stephenson@uwo.ca

 If you have any questions about your rights as a research participant or the conduct of this
study, you may contact The Office of Human Research Ethics (519) 661-3036, 1-844-720-9816,
email: ethics@uwo.ca. This office oversees the ethical conduct of research studies and is not
part of the study team. Everything that you discuss will be kept confidential.

   o I consent to participate in this study. I have read all of the information about the study.
   (1)

   o I do not consent to participate. (2)
cps19_consent

Lettre d'information et de consentement Titre du projet: Étude électorale canadienne
2019
Chercheure principale: Laura Stephenson, PhD, Science politique, University of Western
Ontario, (519) 661-2111 x 85164, laura.stephenson@uwo.ca
Co-chercheurs: Allison Harell, PhD, Science politique, Université du Québec à Montréal, (514)
987-3000 x 5676, harell.allison@uqam.ca
Peter Loewen, PhD, Science politique, Munk School of Global Affairs and Public Policy,
University of Toronto, (416) 978-5120, peter.loewen@utoronto.ca
Daniel Rubenson, PhD, Politiques et administration publique, Ryerson University, (416) 979-
5000 x 4052, rubenson@ryerson.ca

 Merci de bien vouloir participer à notre sondage. Vous pouvez compléter ce sondage en
français ou en anglais. Veuillez sélectionner la langue de votre choix à l'aide du menu déroulant
dans le coin supérieur droit de l'écran. (You can complete the survey in English or in
French. Please choose your preferred language using the drop-down menu at the top right of
this screen).

 Nous effectuons une étude portant sur l'attitude des Canadiens au sujet de l'actualité, des
élections et de la démocratie, et nous aimerions connaître votre opinion. Votre participation est
volontaire. Vos réponses demeureront confidentielles et ne seront utilisées qu’à des fins de
recherche. Pour participer, vous devez avoir au moins 18 ans et avoir un statut juridique au
Canada.




                                                                                                   37
Ce sondage prendra environ 20 minutes à compléter. Si vous participez aujourd'hui, il est
possible que vous soyez recontacté à une date ultérieure et invité à remplir d'autres sondages.
Votre participation sera également volontaire.

 Pour obtenir des informations supplémentaires sur cette étude, sur vos droits en tant que
participant, sur la compensation offerte en échange de votre temps ainsi que sur la manière
dont les données seront conservées, veuillez cliquer ICI. Pour compléter le sondage, veuillez
cliquer sur le lien ci-dessous.

 Pour toutes questions portant sur l'étude ou ses résultats, vous pouvez contacter en tout
temps:

Dr. Laura Stephenson
Département de science politique
University of Western Ontario
London, Ontario, Canada
1-519-661-2111 ext. 85164
Laura.stephenson@uwo.ca

 Pour toutes questions sur vos droits en tant que participant ou sur le déroulement de cette
étude, vous pouvez contacter le Bureau de l'éthique de la recherche humaine au (519) 661-
3036, 1-844-720-9816, ou par courriel: ethics@uwo.ca. Ce bureau s'assure du respect de
l'éthique et ne fait pas partie de l'équipe de recherche. Tout ce dont vous discuterez demeurera
confidentiel.

    o Je consens à participer à cette étude. J'ai lu toutes les informations sur l'étude. (1)
    o Je ne consens pas à participer. (2)
Skip To: End of Block If Letter of Information and Consent Project Title: Canadian Election Study
2019Principal Investigat... != I consent to participate in this study. I have read all of the information about
the study.


NOTE: The “HERE” text (or “ICI” in the French side) in the consent
page led to another page, which would open in a new browser window or
tab, that contained the text below.6

6
 This separate page was implemented as a separate survey in the Qualtrics platform, so that it could open in a new
window, and not have the respondent lose their place in the current survey session. Here’s how to set it up:

1. Create a separate survey for the additional information page, format and publish it

2. Add a hyperlink to the main consent page, that goes to the live survey link for the additional page. Make sure to set
the link to open in a new window (it's under the "edit link" options when you right-click on the link), so that they don't
lose their spot in the survey.




                                                                                                                       38
NOTE: Respondents who did not consent to the survey were screened out.




additional_consent
Letter of Information and Consent – Additional Information
 Project Title: Canadian Election Study 2019
 Principal Investigator: Laura Stephenson, PhD, Political Science, University of Western
Ontario, (519) 661-2111x85164, laura.stephenson@uwo.ca
 Co-Investigators: Allison Harell, PhD, Political Science, Université de Québec à Montréal,
(514) 987-3000 x5676, harell.allison@uqam.ca
 Peter Loewen, PhD, Political Science, Munk School of Global Affairs, University of Toronto,
(416) 978-5120, peter.loewen@utoronto.ca
 Daniel Rubenson, PhD, Politics and Public Administration, Ryerson University, (416) 979-5000
x 4052, rubenson@ryerson.ca
 Funding: This project is funded by the Social Sciences and Humanities Research Council of
Canada.

The purpose of this screen is to provide you with information about the research study you are
being invited to participate in. You must be 18 years of age or older and a legal resident of
Canada to be eligible to participate.

 The purpose of the study is to obtain information about your views regarding current events,
elections and democracy in Canada. Your participation in this study is voluntary. You may
decide not to be in this study. Even if you consent to participate you have the right to not answer
individual questions or to withdraw from the study at any time. If you choose not to participate or
to leave the study at any time it will have no effect on you. If you decide to withdraw from the
study, you may do so at any time by exiting the survey window. Due to the anonymous nature of
your data, once your survey responses have been submitted, the researchers will be unable to
withdraw your data.

 Your survey responses will be collected anonymously through a secure online survey platform
called Qualtrics. Qualtrics uses encryption technology and restricted access authorizations to
protect all data collected. In addition, Western’s Qualtrics server is in Ireland, where privacy
standards are maintained under the EU-US Privacy Shield. The data will then be exported from


3. If you want to have the link go to the same language as the source page, you have to add "?Q_Language=EN" or
"?Q_Language=FR" (or whatever Qualtrics language codes are relevant).

JavaScript was added to remove the "next" button on the additional info page, so that they could only view the page,
not "complete" that survey and get to a completion page that might confuse them.


                                                                                                                  39
Qualtrics and securely stored on Western University's server.

 The survey you are being asked to complete today will take about 20 minutes to
complete. Should you complete today’s survey, you may be re-contacted and asked to
participate in additional surveys as well. Participation today does not commit you to complete
any additional surveys.

 The benefit of participating in our study is that your responses will help us to know more about
democracy in Canada. You may not benefit personally from your participation. There are no
known risks or discomforts associated with participating in this study.

We do not offer any compensation for your participation today, however if you are eligible to
participate and submit the survey then you may be eligible for compensation from Qualtrics, as
determined by their current policies.

 Your confidentiality will be maintained at all times. Representatives of Western University’s
Non-Medical Research Ethics Board may require access to your study-related records to
monitor the conduct of the research. The data will be stored on a secure server at Western
University and will be retained for a minimum of 7 years. Your data may be archived and
retained indefinitely and could be used for future research purposes (e.g., to answer a new
research question). By consenting to participate in this study, you are agreeing that your data
can be used beyond the purposes of this present study by either the current or other
researchers.

 All identifiable information will be deleted from the dataset collected so that individual
participants’ anonymity will be protected. The de-identified data will be accessible by the study
investigators as well as the broader scientific community. More specifically, the data will be
made publicly available so that data may be inspected and analyzed by others. The data that
will be shared in the dataset will not contain any information that can identify you.

You do not waive any legal right by participating in this study.

If you have questions at any time about the study or its results, you may contact:
Dr. Laura Stephenson
Department of Political Science
University of Western Ontario
London, Ontario, Canada
1-519-661-2111 ext. 85164
Laura.stephenson@uwo.ca

 If you have any questions about your rights as a research participant or the conduct of this
study, you may contact The Office of Human Research Ethics (519) 661-3036, 1-844-720-9816,
email: ethics@uwo.ca. This office oversees the ethical conduct of research studies and is not
part of the study team. Everything that you discuss will be kept confidential.


                                                                                                  40
Completion of the survey indicates your consent to participate.

 If you wish to participate in this phase of the study, please close this window and indicate your
consent to begin the survey.

additional_consent
Lettre d’information et formulaire de consentement - Informations supplémentaires

Titre du projet: Étude électorale canadienne de 2019
Chercheure principale: Laura Stephenson, PhD, Science politique, University of Western
Ontario, (519) 661-2111x85164, laura.stephenson@uwo.ca
Co-chercheurs: Allison Harell, PhD, Science politique, Université de Québec à Montréal, (514)
987-3000 x5676, harell.allison@uqam.ca
Peter Loewen, PhD, Science politique, Munk School of Global Affairs and Public Policy,
University of Toronto, (416) 978-5120, peter.loewen@utoronto.ca
Daniel Rubenson, PhD, Politiques et administration publique, Ryerson University, (416) 979-
5000 x 4052, rubenson@ryerson.ca
Financement: Ce projet est financé par le Conseil de recherches en sciences humaines du
Canada.

 L’objectif de cette page est de vous fournir de l’information concernant l’étude pour laquelle
vous êtes invité à participer. Pour être eligible à participer, vous devez avoir 18 ans ou plus et
être un résident avec un statut juridique au Canada.

Le but de cette étude est de mieux connaître votre opinion sur l’actualité, les élections et la
démocratie au Canada. Votre participation à cette étude est volontaire, donc vous pouvez
décider de ne pas y participer. Même si vous décidez de participer, vous avez le droit de ne pas
répondre à certaines questions ou de vous retirer de l’étude en tous temps. Si vous ne
participez pas ou décidez de vous retirer de l’étude, cette décision n’aura aucune conséquence
sur vous. Si vous décidez de vous retirer de l’étude, vous pouvez le faire en tout temps
simplement en ferment la page du questionnaire. En raison de la nature anonyme de vos
données, une fois que vos réponses au sondage auront été soumises, les chercheurs ne
pourront pas retirer vos données.

 Vos réponses seront recueillies de manière anonyme via une plateforme d’enquête en ligne
sécurisée. Cette plateforme, nommée Qualtrics, utilise des mesures d’encryptage et des accès
restreints par autorization pour protéger les données. De plus, le serveur Western de Qualtrics
se retrouve en Irlande, où les standards de protection de la vie privée sont établis sous le
bouclier UE-États-Unis (EU-US Privacy Shield). Les données seront ensuite exportées de
Qualtrics et stockées de manière sécurisée sur le serveur de Western University.

 Le sondage que vous êtes invité à compléter aujourd'hui prendra environ 20 minutes. Si vous
le complétez, il est possible que vous soyez recontacté à une date ultérieure et invité à remplir


                                                                                                     41
d’autres sondages. Votre participation à ces sondages sera également volontaire.

 L’avantage de participer à cette étude est que vos réponses nous aideront à mieux comprendre
la démocratie au Canada. Vous ne bénéficerez pas directement de votre participation. Il n’y a
pas de risques ou d’inconforts liés à votre participation à cette étude.

 Nous n’offrons aucune compensation pour votre participation aujourd’hui. Cependant, si vous
êtes éligible à participer et à soumettre le sondage, vous pourriez être éligible à une
indemnisation de la part de Qualtrics, tel que déterminé par leurs politiques en vigueur.

 Votre confidentialité sera maintenue en tout temps. Les représentants du comité d’éthique de la
recherche non médicale de Western University peuvent avoir besoin d’accéder à vos dossiers
en lien avec l’étude afin de suivre la conduite de la recherche. Les données seront stockées
sur un serveur sécurisé de Western University et seront conservées pendant au moins 7 ans.
Vos données peuvent être archivées et conservées indéfiniment et peuvent être utilisées à des
fins de recherche future (par exemple, pour répondre à une nouvelle question de recherche). En
consentant à participer à cette étude, vous acceptez que vos données puissent être utilisées
au-delà des objectifs de la présente étude par le chercheur actuel ou par d’autres chercheurs.

Toutes les informations pouvant vous identifier seront supprimées de l’ensemble des données
collectées afin que l’anonymat des participants soit protégé. Les données anonymisées seront
accessibles aux chercheurs de l’étude ainsi qu’à la communauté scientifique. De manière plus
spécifique, les données seront rendues publiques afin qu’elles puissent être examinées et
analysées par d’autres. Les données qui seront partagées dans le jeu de données ne
contiendront aucune information permettant de vous identifier.

Vous ne renoncez à aucun droit légal en participant à cette étude.

 Si vous avez des questions portant sur l’étude ou ses résultats, vous pouvez contacter en tout
temps:
 Dr. Laura Stephenson
 Département de science politique
 University of Western Ontario
London, Ontario, Canada
 1-519-661-2111 ext. 85164
 Laura.stephenson@uwo.ca

 Si vous avez des questions sur vos droits en tant que participant à la recherche ou sur la
conduite de cette étude, vous pouvez contacter le Bureau de l’éthique de la recherche humaine
au (519) 661-3036, 1-844-720-9816, our par courriel: ethics@uwo.ca. Ce bureau supervise la
conduite éthique d’études en recherche et ne fait pas partie de l’équipe de recherche. Tout ce
dont vous discutez restera confidentiel.

En répondant au questionnaire, vous indiquez votre consentement à participer à l'étude.


                                                                                              42
 Si vous souhaitez participer à cette phase de l’étude, veuillez fermer cette fenêtre et indiquer
votre consentement à débuter l’enquête.



Page Break




cps19_captcha Before you proceed to the survey, please complete the Captcha below.

cps19_captcha Avant d’accéder au sondage, veuillez compléter le Captcha ci-dessous.



Page Break




                                                                                                    43
cps19_citizenship Are you a...

    o Canadian citizen (4)
    o Permanent resident (5)
    o Other (6)
cps19_citizenship Êtes-vous...

    o Citoyen canadien (4)
    o Résident permanent (5)
    o Autre (6)
Skip To: End of Block If Are you a... = Other


NOTE: Respondents who responded with an “Other” citizenship were
screened out of the survey.


Page Break




                                                                   44
45
cps19_yob To make sure we are talking to a cross section of Canadians, we need to get a little
information about your background. First, in what year were you born?

   o 1920 (1)
   o 1921 (2)
   o 1922 (3)
   o 1923 (4)
   o 1924 (5)
   o 1925 (6)
   o 1926 (7)
   o 1927 (8)
   o 1928 (9)
   o 1929 (10)
   o 1930 (11)
   o 1931 (12)
   o 1932 (13)
   o 1933 (14)
   o 1934 (15)
   o 1935 (16)
   o 1936 (17)
   o 1937 (18)
   o 1938 (19)
                                                                                            46
o 1939 (20)
o 1940 (21)
o 1941 (22)
o 1942 (23)
o 1943 (24)
o 1944 (25)
o 1945 (26)
o 1946 (27)
o 1947 (28)
o 1948 (29)
o 1949 (30)
o 1950 (31)
o 1951 (32)
o 1952 (33)
o 1953 (34)
o 1954 (35)
o 1955 (36)
o 1956 (37)
o 1957 (38)
o 1958 (39)
              47
o 1959 (40)
o 1960 (41)
o 1961 (42)
o 1962 (43)
o 1963 (44)
o 1964 (45)
o 1965 (46)
o 1966 (47)
o 1967 (48)
o 1968 (49)
o 1969 (50)
o 1970 (51)
o 1971 (52)
o 1972 (53)
o 1973 (54)
o 1974 (55)
o 1975 (56)
o 1976 (57)
o 1977 (58)
o 1978 (59)
              48
o 1979 (60)
o 1980 (61)
o 1981 (62)
o 1982 (63)
o 1983 (64)
o 1984 (65)
o 1985 (66)
o 1986 (67)
o 1987 (68)
o 1988 (69)
o 1989 (70)
o 1990 (71)
o 1991 (72)
o 1992 (73)
o 1993 (74)
o 1994 (75)
o 1995 (76)
o 1996 (77)
o 1997 (78)
o 1998 (79)
              49
   o 1999 (80)
   o 2000 (81)
   o 2001 (82)
   o 2002 (83)
   o 2003 (84)
   o 2004 (85)
   o 2005 (86)
   o 2006 (87)
   o 2007 (88)
   o 2008 (89)
   o 2009 (90)
   o 2010 (91)
cps19_yob
Afin d’être certains que nous nous adressons à un échantillon représentatif des Canadiens,




                                                                                             50
nous avons besoin d’informations de base sur vous. Tout d'abord, en quelle année êtes-vous
né(e)?

   o 1920 (1)
   o 1921 (2)
   o 1922 (3)
   o 1923 (4)
   o 1924 (5)
   o 1925 (6)
   o 1926 (7)
   o 1927 (8)
   o 1928 (9)
   o 1929 (10)
   o 1930 (11)
   o 1931 (12)
   o 1932 (13)
   o 1933 (14)
   o 1934 (15)
   o 1935 (16)
   o 1936 (17)
   o 1937 (18)
   o 1938 (19)
                                                                                             51
o 1939 (20)
o 1940 (21)
o 1941 (22)
o 1942 (23)
o 1943 (24)
o 1944 (25)
o 1945 (26)
o 1946 (27)
o 1947 (28)
o 1948 (29)
o 1949 (30)
o 1950 (31)
o 1951 (32)
o 1952 (33)
o 1953 (34)
o 1954 (35)
o 1955 (36)
o 1956 (37)
o 1957 (38)
o 1958 (39)
              52
o 1959 (40)
o 1960 (41)
o 1961 (42)
o 1962 (43)
o 1963 (44)
o 1964 (45)
o 1965 (46)
o 1966 (47)
o 1967 (48)
o 1968 (49)
o 1969 (50)
o 1970 (51)
o 1971 (52)
o 1972 (53)
o 1973 (54)
o 1974 (55)
o 1975 (56)
o 1976 (57)
o 1977 (58)
o 1978 (59)
              53
o 1979 (60)
o 1980 (61)
o 1981 (62)
o 1982 (63)
o 1983 (64)
o 1984 (65)
o 1985 (66)
o 1986 (67)
o 1987 (68)
o 1988 (69)
o 1989 (70)
o 1990 (71)
o 1991 (72)
o 1992 (73)
o 1993 (74)
o 1994 (75)
o 1995 (76)
o 1996 (77)
o 1997 (78)
o 1998 (79)
              54
    o 1999 (80)
    o 2000 (81)
    o 2001 (82)
    o 2002 (83)
    o 2003 (84)
    o 2004 (85)
    o 2005 (86)
    o 2006 (87)
    o 2007 (88)
    o 2008 (89)
    o 2009 (90)
    o 2010 (91)
Skip To: End of Block If To make sure we are talking to a cross section of Canadians, we need to get a
little information... = 2002
Skip To: End of Block If To make sure we are talking to a cross section of Canadians, we need to get a
little information... = 2003
Skip To: End of Block If To make sure we are talking to a cross section of Canadians, we need to get a
little information... = 2004
Skip To: End of Block If To make sure we are talking to a cross section of Canadians, we need to get a
little information... = 2005
Skip To: End of Block If To make sure we are talking to a cross section of Canadians, we need to get a
little information... = 2006
Skip To: End of Block If To make sure we are talking to a cross section of Canadians, we need to get a
little information... = 2007
Skip To: End of Block If To make sure we are talking to a cross section of Canadians, we need to get a
little information... = 2008
Skip To: End of Block If To make sure we are talking to a cross section of Canadians, we need to get a
little information... = 2009




                                                                                                         55
Skip To: End of Block If To make sure we are talking to a cross section of Canadians, we need to get a
little information... = 2010


NOTE: Respondents who were born in 2002 or later were screened out of
the survey. Respondents who were born in 2001 received an additional
question to determine whether they were 18 years of age or not.


Page Break




                                                                                                         56
Display This Question:
    If To make sure we are talking to a cross section of Canadians, we need to get a little information... =
2001


cps19_yob_2001_age How old are you?

    o 17 (1)
    o 18 (2)
cps19_yob_2001_age Quel âge avez-vous?

    o 17 (1)
    o 18 (2)
Skip To: End of Block If How old are you? = 17
NOTE: Respondents who were 17 years old were screened out of the
survey.


Page Break




                                                                                                         57
cps19_gender Are you...

   o A man (1)
   o A woman (2)
   o Other (e.g. Trans, non-binary, two-spirit, gender-queer) (3)
cps19_gender Êtes-vous...

   o Un homme (1)
   o Une femme (2)
   o Autre (ex: Trans, non-binaire, bispirituel, gender-queer) (3)
Page Break




                                                                     58
cps19_province Which province or territory are you currently living in?

   o Alberta (14)
   o British Columbia (15)
   o Manitoba (16)
   o New Brunswick (17)
   o Newfoundland and Labrador (18)
   o Northwest Territories (19)
   o Nova Scotia (20)
   o Nunavut (21)
   o Ontario (22)
   o Prince Edward Island (23)
   o Quebec (24)
   o Saskatchewan (25)
   o Yukon (26)




                                                                          59
cps19_province Dans quelle province ou territoire habitez-vous présentement?




   o Alberta (14)
   o Colombie-Britannique (15)
   o Manitoba (16)
   o Nouveau-Brunswick (17)
   o Terre-Neuve-et-Labrador (18)
   o Territoires du Nord-Ouest (19)
   o Nouvelle-Écosse (20)
   o Nunavut (21)
   o Ontario (22)
   o Île-du-Prince-Édouard (23)
   o Québec (24)
   o Saskatchewan (25)
   o Yukon (26)
Page Break




                                                                               60
NOTE: Respondents’ full 6-digit postal code was collected, and used to
determine their riding, but not distributed with the data. The first
three digits of their postal code are available however, in the
variable cps19_fsa (available upon request).

cps19_postalcode Please enter your six-digit postal code in the box below. (For example "A1A
1A1", with letters in uppercase)

We are collecting your postal code in order to compare our results to census and electoral
district data. Your postal code will not be released publicly or shared with any third party.

    ________________________________________________________________

cps19_postalcode Veuillez inscrire votre code postal à six chiffres dans la case ci-dessous. (Par
exemple, "A1A 1A1", avec des lettres majuscules)


Nous recueillons votre code postal afin de comparer nos résultats aux données de recensement
et de circonscription. Votre code postal ne sera pas divulgué publiquement ni partagé avec des
tiers.

    ________________________________________________________________



Page Break




                                                                                                61
cps19_education What is the highest level of education that you have completed?

   o No schooling (1)
   o Some elementary school (2)
   o Completed elementary school (3)
   o Some secondary/ high school (4)
   o Completed secondary/ high school (5)
   o Some technical, community college, CEGEP, College Classique (6)
   o Completed technical, community college, CEGEP, College Classique (7)
   o Some university (8)
   o Bachelor's degree (9)
   o Master's degree (10)
   o Professional degree or doctorate (11)
   o Don't know/ Prefer not to answer (12)




                                                                                  62
cps19_education Quel est votre plus haut niveau de scolarité complété?

   o Aucune scolarité (1)
   o Quelques années d'école primaire (2)
   o École primaire terminée (3)
   o Quelques années d'école secondaire (4)
   o École secondaire terminée (5)
   o Quelques années d'études au collègue, au cégep ou au collège classique (6)
   o Études terminées au collège, au cégep, ou au collège classique (7)
   o Quelques années d'études universitaires (8)
   o Baccalauréat (9)
   o Maîtrise (10)
   o Diplôme professionnel ou doctorat (11)
   o Ne sais pas/Préfère ne pas répondre (12)
End of Block: Consent and quota demographics



   8.3.2      Democracy, voting, and parties
Start of Block: Democracy, voting, and parties




                                                                                  63
cps19_demsat On the whole, how satisfied are you with the way democracy works in Canada?

   o Very satisfied (1)
   o Fairly satisfied (2)
   o Not very satisfied (3)
   o Not at all satisfied (4)
   o Don't know/ Prefer not to answer (5)
cps19_demsat Dans l'ensemble, quel est votre niveau de satisfaction quant au fonctionnement
de la démocratie au Canada?

   o Très satisfait (1)
   o Assez satisfait (2)
   o Pas très satisfait (3)
   o Pas du tout satisfait (4)
   o Je ne sais pas/Préfère ne pas répondre (5)
Page Break




                                                                                         64
cps19_imp_iss What is the most important issue to you personally in this federal election?

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

cps19_imp_iss Quel est l'enjeu le plus important, pour vous personnellement, dans cette
élection fédérale?

Si vous ne savez pas, ou préférez ne pas répondre, veuillez appuyer sur →

    ________________________________________________________________



Page Break




                                                                                             65
Display This Question:
    If If What is the most important issue to you personally in this federal election?If you do not know, o...
Text Response Is Not Empty




cps19_imp_iss_party Which party is best at addressing this issue?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
    o Bloc Québécois (4)
    o Green Party (5)
    o People's Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o Don't know/ Prefer not to answer (8)




                                                                                                           66
cps19_imp_iss_party Quel parti aborde le mieux cet enjeu?

   o Parti libéral (1)
   o Parti conservateur (2)
   o NPD (3)
   o Bloc québécois (4)
   o Parti vert (5)
   o Parti populaire (6)
   o Autre parti (veuillez spécifier) (7)
   ________________________________________________

   o Je ne sais pas/Préfère ne pas répondre (8)
Page Break




                                                            67
NOTE: cps19_imp_loc_iss was set to receive a split sample of 50%
(1/2), to make room in the survey for more questions. Whether a
respondent was assigned to receive cps19_imp_loc_iss was randomly
determined in the Survey Flow by setting the embedded data field
get_imp_loc_iss to either 0 or 1. If get_imp_loc_iss was equal to 1,
they were assigned to receive cps19_imp_loc_iss. get_imp_loc_iss can
be used to filter the dataset to only respondents that were assigned
to receive cps19_imp_loc_iss.




Display This Question:
    If get_imp_loc_iss = 1


cps19_imp_loc_iss What is the most important local issue to you personally in this federal
election?

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

cps19_imp_loc_iss
Quel est l'enjeu local le plus important, pour vous personnellement, dans cette élection
fédérale?
 Si vous ne savez pas, ou préférez ne pas répondre, veuillez sélectionner →

    ________________________________________________________________



Page Break




                                                                                             68
Display This Question:
    If If What is the most important local issue to you personally in this federal election? If you do not
know, or prefer not to answer, please click → Text Response Is Not Empty
Carry Forward All Choices - Displayed & Hidden from "Which party is best at addressing this issue?"




cps19_imp_loc_iss_p Which party is best at addressing this local issue?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
    o Bloc Québécois (4)
    o Green Party (5)
    o People's Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o Don't know/ Prefer not to answer (8)




                                                                                                             69
cps19_imp_loc_iss_p Quel parti aborde le mieux cet enjeu local?

   o Parti libéral (1)
   o Parti conservateur (2)
   o NPD (3)
   o Bloc québécois (4)
   o Parti vert (5)
   o Parti populaire (6)
   o Autre parti (veuillez spécifier) (7)
   ________________________________________________

   o Je ne sais pas/Préfère ne pas répondre (8)
Page Break




                                                                  70
cps19_interest_gen How interested are you in politics generally? Set the slider to a number
from 0 to 10, where 0 means no interest at all, and 10 means a great deal of interest.

If you do not know, or prefer not to answer, please click →
                                                  No interest at A great deal of       Don't know/
                                                        all         interest           Prefer not to
                                                                                         answer

                                                 0    1   2      3   4   5   6     7     8    9   10

                                      &nbsp ()




cps19_interest_gen Quel est votre intérêt pour la politique en général? Veuillez glisser la
barre sur un chiffre de 0 à 10, où 0 indique aucun intérêt du tout et 10 indique beaucoup
d'intérêt.


Si vous ne savez pas, ou préférez ne pas répondre, veuillez appuyer sur →


                                                 Aucun intérêt       Beaucoup        Je ne sais
                                                                      d'intérêt    pas/Préfère ne
                                                                                    pas répondre

                                                 0    1   2      3   4   5   6     7     8    9   10

                                      &nbsp ()




Page Break




                                                                                                   71
cps19_interest_elxn How interested are you in this federal election? Set the slider to a number
from 0 to 10, where 0 means no interest at all, and 10 means a great deal of interest.

If you do not know, or prefer not to answer, please click →
                                                  No interest at A great deal of       Don't know/
                                                        all         interest           Prefer not to
                                                                                         answer

                                                  0   1    2   3    4   5    6     7     8    9   10

                                      &nbsp ()




cps19_interest_elxn Quel est votre intérêt pour cette élection fédérale? Veuillez glisser la barre
sur un chiffre de 0 à 10, où 0 indique aucun intérêt du tout et 10 indique beaucoup d'intérêt.
                                                  Aucun intérêt       Beaucoup      Je ne sais
                                                                       d'intérêt  pas/Préfère ne
                                                                                   pas répondre

                                                  0   1    2   3    4   5    6     7     8    9   10

                                      &nbsp ()




Page Break




                                                                                                   72
Display This Question:
    If Are you a... = Canadian citizen


cps19_v_likely On election day, are you...

   o Certain to vote (1)
   o Likely to vote (2)
   o Unlikely to vote (3)
   o Certain not to vote (4)
   o I am not eligible to vote (5)
   o I voted in an advance poll (7)
   o Don't know/ Prefer not to answer (6)
cps19_v_likely Lors du jour de l'élection, quelle option vous décrit le mieux?

   o Certain(e) de voter (1)
   o Probable de voter (2)
   o Improbable de voter (3)
   o Certain(e) de ne pas voter (4)
   o Je ne suis pas éligible au vote (5)
   o J'ai voté par anticipation (7)
   o Je ne sais pas/Préfère ne pas répondre (6)


                                                                                 73
Page Break




             74
Display This Question:
    If Are you a... = Permanent resident


cps19_v_likely_pr If you become a Canadian citizen, how likely are you to vote in the first
election for which you are eligible?

   o Certain to vote (1)
   o Likely to vote (2)
   o Unlikely to vote (3)
   o Certain not to vote (4)
   o Don't know/ Prefer not to answer (5)
cps19_v_likely_pr Si vous devenez citoyen canadien, quelle est la probabilité que vous votiez à
la première élection à laquelle vous êtes admissible?

   o Certain(e) de voter (1)
   o Probable de voter (2)
   o Improbable de voter (3)
   o Certain(e) de ne pas voter (4)
   o Je ne sais pas/Préfère ne pas répondre (5)
Page Break




                                                                                              75
Display This Question:
    If On election day, are you... = Certain to vote
    Or On election day, are you... = Likely to vote
And If
    Are you a... = Canadian citizen




cps19_votechoice Which party do you think you will vote for?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
Which province or territory are you currently living in? = Quebec

    o Bloc Québécois (4)
    o Green Party (5)
    o People's Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o Don't know/ Prefer not to answer (9)




                                                                    76
cps19_votechoice Pour quel parti prévoyez-vous voter?

    o Parti libéral (1)
    o Parti conservateur (2)
    o NPD (3)
Which province or territory are you currently living in? = Quebec

    o Bloc québécois (4)
    o Parti vert (5)
    o Parti populaire (6)
    o Autre parti (veuillez spécifier) (7)
    ________________________________________________

    o Je ne sais pas/Préfère ne pas répondre (9)
Page Break




                                                                    77
Display This Question:
    If If you become a Canadian citizen, how likely are you to vote in the first election for which you... =
Certain to vote
     Or If you become a Canadian citizen, how likely are you to vote in the first election for which you... =
Likely to vote
Or If
        On election day, are you... = I am not eligible to vote




cps19_votechoice_pr If you could vote in this election, which party do you think you would vote
for?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
Which province or territory are you currently living in? = Quebec

    o Bloc Québécois (4)
    o Green Party (5)
    o People's Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o Don't know/ Prefer not to answer (9)




                                                                                                           78
cps19_votechoice_pr Si vous pouviez voter lors de cette élection, pour quel parti voteriez-vous?

    o Parti libéral (1)
    o Parti conservateur (2)
    o NPD (3)
Which province or territory are you currently living in? = Quebec

    o Bloc québécois (4)
    o Parti vert (5)
    o Parti populaire (6)
    o Autre parti (veuillez spécifier) (7)
    ________________________________________________

    o Je ne sais pas/Préfère ne pas répondre (9)
Page Break




                                                                                             79
Display This Question:
    If On election day, are you... = Unlikely to vote
And If
    Are you a... = Canadian citizen




cps19_vote_unlikely If you decide to vote, which party do you think you will vote for?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
Which province or territory are you currently living in? = Quebec

    o Bloc Québécois (4)
    o Green Party (5)
    o People's Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o Don't know/ Prefer not to answer (9)




                                                                                         80
cps19_vote_unlikely Si vous décidez de voter, pour quel parti prévoyez-vous voter?

    o Parti libéral (1)
    o Parti conservateur (2)
    o NPD (3)
Which province or territory are you currently living in? = Quebec

    o Bloc québécois (4)
    o Parti vert (5)
    o Parti populaire (6)
    o Autre parti (veuillez spécifier) (7)
    ________________________________________________

    o Je ne sais pas/Préfère ne pas répondre (9)
Page Break




                                                                                     81
Display This Question:
     If If you become a Canadian citizen, how likely are you to vote in the first election for which you... =
Unlikely to vote
    Or If you become a Canadian citizen, how likely are you to vote in the first election for which you... =
Don't know/ Prefer not to answer




cps19_vote_unlike_pr If you could vote in this election, and decided to vote, which party do you
think you would vote for?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
Which province or territory are you currently living in? = Quebec

    o Bloc Québécois (4)
    o Green Party (5)
    o People's Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o Don't know/ Prefer not to answer (9)




                                                                                                            82
cps19_vote_unlike_pr Si vous pouviez voter lors de cette élection et que vous décidiez de voter,
pour quel parti voteriez-vous?

    o Parti libéral (1)
    o Parti conservateur (2)
    o NPD (3)
Which province or territory are you currently living in? = Quebec

    o Bloc québécois (4)
    o Parti vert (5)
    o Parti populaire (6)
    o Autre parti (veuillez spécifier) (7)
    ________________________________________________

    o Je ne sais pas/Préfère ne pas répondre (9)
Page Break




                                                                                             83
Display This Question:
    If On election day, are you... = I voted in an advance poll
And If
    Are you a... = Canadian citizen




cps19_v_advance For which party did you vote?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
Which province or territory are you currently living in? = Quebec

    o Bloc Québécois (4)
    o Green Party (5)
    o People's Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o Don't know/ Prefer not to answer (9)




                                                                    84
cps19_v_advance Pour quel parti avez-vous voté?

    o Parti libéral (1)
    o Parti conservateur (2)
    o NPD (3)
Which province or territory are you currently living in? = Quebec

    o Bloc québécois (4)
    o Parti vert (5)
    o Parti populaire (6)
    o Autre parti (veuillez spécifier) (7)
    ________________________________________________

    o Je ne sais pas/Préfère ne pas répondre (9)
Page Break




                                                                    85
Display This Question:
    If On election day, are you... = Don't know/ Prefer not to answer
And If
    Are you a... = Canadian citizen




cps19_vote_lean Is there a party you are leaning towards?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
Which province or territory are you currently living in? = Quebec

    o Bloc Québécois (4)
    o Green Party (5)
    o People's Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o I do not intend to vote (8)
    o Don't know/ Prefer not to answer (9)




                                                                        86
cps19_vote_lean Êtes-vous tenté(e) d'appuyer un parti en particulier?

    o Parti libéral (1)
    o Parti conservateur (2)
    o NPD (3)
Which province or territory are you currently living in? = Quebec

    o Bloc québécois (4)
    o Parti vert (5)
    o Parti populaire (6)
    o Autre parti (veuillez spécifier) (7)
    ________________________________________________

    o Je ne prévois pas voter (8)
    o Je ne sais pas/Préfère ne pas répondre (9)
Page Break




                                                                        87
Display This Question:
    If If you become a Canadian citizen, how likely are you to vote in the first election for which you... =
Don't know/ Prefer not to answer




cps19_vote_lean_pr If you could vote in this election, is there a party you would be leaning
towards?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
Which province or territory are you currently living in? = Quebec

    o Bloc Québécois (4)
    o Green Party (5)
    o People's Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o I do not intend to vote (8)
    o Don't know/ Prefer not to answer (9)




                                                                                                           88
cps19_vote_lean_pr Si vous pouviez voter lors de l'élection, seriez-vous tenté d'appuyer un
parti en particulier?

    o Parti libéral (1)
    o Parti conservateur (2)
    o NPD (3)
Which province or territory are you currently living in? = Quebec

    o Bloc québécois (4)
    o Parti vert (5)
    o Parti populaire (6)
    o Autre parti (veuillez spécifier) (7)
    ________________________________________________

    o Je ne prévois pas voter (8)
    o Je ne sais pas/Préfère ne pas répondre (9)
Page Break




                                                                                              89
Display This Question:
    If On election day, are you... = Certain to vote
    Or On election day, are you... = Likely to vote
    And Which party do you think you will vote for? != Don't know/ Prefer not to answer




cps19_2nd_choice And which party would be your second choice?
Which party do you think you will vote for? != Liberal Party

    o Liberal Party (1)
Which party do you think you will vote for? != Conservative Party

    o Conservative Party (2)
Which party do you think you will vote for? != NDP

    o NDP (3)
Which province or territory are you currently living in? = Quebec

    o Bloc Québécois (4)
Which party do you think you will vote for? != Green Party

    o Green Party (5)
Which party do you think you will vote for? != People's Party

    o People's Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o Don't know/ Prefer not to answer (9)




                                                                                          90
cps19_2nd_choice Et quel parti serait votre deuxième choix?
Which party do you think you will vote for? != Liberal Party

    o Parti libéral (1)
Which party do you think you will vote for? != Conservative Party

    o Parti conservateur (2)
Which party do you think you will vote for? != NDP

    o NPD (3)
Which province or territory are you currently living in? = Quebec

    o Bloc québécois (4)
Which party do you think you will vote for? != Green Party

    o Parti vert (5)
Which party do you think you will vote for? != People's Party

    o Parti populaire (6)
    o Autre parti (veuillez spécifier) (7)
    ________________________________________________

    o Je ne sais pas/Préfère ne pas répondre (9)
Page Break




                                                                    91
Display This Question:
    If If you become a Canadian citizen, how likely are you to vote in the first election for which you... =
Certain to vote
     Or If you become a Canadian citizen, how likely are you to vote in the first election for which you... =
Likely to vote
Or If
        On election day, are you... = I am not eligible to vote
And If
     If you could vote in this election, which party do you think you would vote for? != Don't know/ Prefer
not to answer




                                                                                                           92
cps19_2nd_choice_pr And which party would be your second choice?
If you could vote in this election, which party do you think you would vote for? != Liberal Party

    o Liberal Party (1)
If you could vote in this election, which party do you think you would vote for? != Conservative Party

    o Conservative Party (2)
If you could vote in this election, which party do you think you would vote for? != NDP

    o NDP (3)
Which province or territory are you currently living in? = Quebec

    o Bloc Québécois (4)
If you could vote in this election, which party do you think you would vote for? != Green Party

    o Green Party (5)
If you could vote in this election, which party do you think you would vote for? != People's Party

    o People's Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o Don't know/ Prefer not to answer (9)




                                                                                                         93
cps19_2nd_choice_pr Et quel parti serait votre deuxième choix?
If you could vote in this election, which party do you think you would vote for? != Liberal Party

    o Parti libéral (1)
If you could vote in this election, which party do you think you would vote for? != Conservative Party

    o Parti conservateur (2)
If you could vote in this election, which party do you think you would vote for? != NDP

    o NPD (3)
Which province or territory are you currently living in? = Quebec

    o Bloc québécois (4)
If you could vote in this election, which party do you think you would vote for? != Green Party

    o Parti vert (5)
If you could vote in this election, which party do you think you would vote for? != People's Party

    o Parti populaire (6)
    o Autre parti (veuillez spécifier) (7)
    ________________________________________________

    o Je ne sais pas/Préfère ne pas répondre (9)
Page Break




                                                                                                         94
NOTE: cps19_not_vote_for was set to receive a split sample of 50%
(1/2), to make room in the survey for more questions. Whether a
respondent was assigned to receive cps19_not_vote_for was randomly
determined in the Survey Flow by setting the embedded data field
get_not_vote_for to either 0 or 1. If get_not_vote_for was equal to 1,
they were assigned to receive cps19_not_vote_for. get_not_vote_for can
be used to filter the dataset to only respondents that were assigned
to receive cps19_not_vote_for.

Unlike some of the other split sample questions, cps19_not_vote_for
had additional requirements – the respondent had to have indicated
that they might vote in the upcoming election.




Display This Question:
    If get_not_vote_for = 1
And If
    On election day, are you... = Certain to vote
    Or On election day, are you... = Likely to vote
    Or On election day, are you... = Unlikely to vote
    Or On election day, are you... = I am not eligible to vote
    Or On election day, are you... = Don't know/ Prefer not to answer
    Or If you become a Canadian citizen, how likely are you to vote in the first election for which you... =
Certain to vote
     Or If you become a Canadian citizen, how likely are you to vote in the first election for which you... =
Likely to vote




                                                                                                           95
cps19_not_vote_for Are there any parties that you would absolutely not vote for? (Select all that
apply)
Which party do you think you will vote for? != Liberal Party
And If you could vote in this election, which party do you think you would vote for? != Liberal Party
And If you decide to vote, which party do you think you will vote for? != Liberal Party
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
Liberal Party
And Is there a party you are leaning towards? != Liberal Party
And If you could vote in this election, is there a party you would be leaning towards? != Liberal Party
And And which party would be your second choice? != Liberal Party
And And which party would be your second choice? != Liberal Party


    ▢           Liberal Party (1)
Which party do you think you will vote for? != Conservative Party
And If you could vote in this election, which party do you think you would vote for? != Conservative Party
And If you decide to vote, which party do you think you will vote for? != Conservative Party
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
Conservative Party
And Is there a party you are leaning towards? != Conservative Party
And If you could vote in this election, is there a party you would be leaning towards? != Conservative
Party
And And which party would be your second choice? != Conservative Party
And And which party would be your second choice? != Conservative Party


    ▢           Conservative Party (2)
Which party do you think you will vote for? != NDP
And If you could vote in this election, which party do you think you would vote for? != NDP
And If you decide to vote, which party do you think you will vote for? != NDP
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
NDP
And Is there a party you are leaning towards? != NDP
And If you could vote in this election, is there a party you would be leaning towards? != NDP
And And which party would be your second choice? != NDP
And And which party would be your second choice? != NDP


    ▢           NDP (3)
Which party do you think you will vote for? != Bloc Québécois



                                                                                                             96
And If you could vote in this election, which party do you think you would vote for? != Bloc Québécois
And If you decide to vote, which party do you think you will vote for? != Bloc Québécois
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
Bloc Québécois
And Is there a party you are leaning towards? != Bloc Québécois
And If you could vote in this election, is there a party you would be leaning towards? != Bloc Québécois
And And which party would be your second choice? != Bloc Québécois
And And which party would be your second choice? != Bloc Québécois


    ▢           Bloc Québécois (4)
Which party do you think you will vote for? != Green Party
And If you could vote in this election, which party do you think you would vote for? != Green Party
And If you decide to vote, which party do you think you will vote for? != Green Party
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
Green Party
And Is there a party you are leaning towards? != Green Party
And If you could vote in this election, is there a party you would be leaning towards? != Green Party
And And which party would be your second choice? != Green Party
And And which party would be your second choice? != Green Party


    ▢           Green Party (5)
Which party do you think you will vote for? != People's Party
And If you could vote in this election, which party do you think you would vote for? != People's Party
And If you decide to vote, which party do you think you will vote for? != People's Party
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
People's Party
And Is there a party you are leaning towards? != People's Party
And If you could vote in this election, is there a party you would be leaning towards? != People's Party
And And which party would be your second choice? != People's Party
And And which party would be your second choice? != People's Party


    ▢           People's Party (6)


    ▢        Another party (please specify) (7)
    ________________________________________________




                                                                                                             97
▢   ⊗I could vote for any of the parties (8)

▢   ⊗Don't know/ Prefer not to answer (9)




                                               98
cps19_not_vote_for Y a-t-il un ou des partis pour lesquels vous ne voteriez absolument pas?
(Veuillez sélectionner tous les partis qui s'appliquent)
Which party do you think you will vote for? != Liberal Party
And If you could vote in this election, which party do you think you would vote for? != Liberal Party
And If you decide to vote, which party do you think you will vote for? != Liberal Party
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
Liberal Party
And Is there a party you are leaning towards? != Liberal Party
And If you could vote in this election, is there a party you would be leaning towards? != Liberal Party
And And which party would be your second choice? != Liberal Party
And And which party would be your second choice? != Liberal Party


    ▢           Parti libéral (1)
Which party do you think you will vote for? != Conservative Party
And If you could vote in this election, which party do you think you would vote for? != Conservative Party
And If you decide to vote, which party do you think you will vote for? != Conservative Party
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
Conservative Party
And Is there a party you are leaning towards? != Conservative Party
And If you could vote in this election, is there a party you would be leaning towards? != Conservative
Party
And And which party would be your second choice? != Conservative Party
And And which party would be your second choice? != Conservative Party


    ▢           Parti conservateur (2)
Which party do you think you will vote for? != NDP
And If you could vote in this election, which party do you think you would vote for? != NDP
And If you decide to vote, which party do you think you will vote for? != NDP
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
NDP
And Is there a party you are leaning towards? != NDP
And If you could vote in this election, is there a party you would be leaning towards? != NDP
And And which party would be your second choice? != NDP
And And which party would be your second choice? != NDP


    ▢           NPD (3)
Which party do you think you will vote for? != Bloc Québécois



                                                                                                             99
And If you could vote in this election, which party do you think you would vote for? != Bloc Québécois
And If you decide to vote, which party do you think you will vote for? != Bloc Québécois
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
Bloc Québécois
And Is there a party you are leaning towards? != Bloc Québécois
And If you could vote in this election, is there a party you would be leaning towards? != Bloc Québécois
And And which party would be your second choice? != Bloc Québécois
And And which party would be your second choice? != Bloc Québécois


    ▢           Bloc québécois (4)
Which party do you think you will vote for? != Green Party
And If you could vote in this election, which party do you think you would vote for? != Green Party
And If you decide to vote, which party do you think you will vote for? != Green Party
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
Green Party
And Is there a party you are leaning towards? != Green Party
And If you could vote in this election, is there a party you would be leaning towards? != Green Party
And And which party would be your second choice? != Green Party
And And which party would be your second choice? != Green Party


    ▢           Parti vert (5)
Which party do you think you will vote for? != People's Party
And If you could vote in this election, which party do you think you would vote for? != People's Party
And If you decide to vote, which party do you think you will vote for? != People's Party
And If you could vote in this election, and decided to vote, which party do you think you would vote... !=
People's Party
And Is there a party you are leaning towards? != People's Party
And If you could vote in this election, is there a party you would be leaning towards? != People's Party
And And which party would be your second choice? != People's Party
And And which party would be your second choice? != People's Party


    ▢           Parti populaire (6)


    ▢        Autre parti (veuillez spécifier) (7)
    ________________________________________________




                                                                                                         100
  ▢          ⊗Je ne prévois pas voter (8)

  ▢          ⊗Je ne sais pas/Préfère ne pas répondre (9)

Page Break




                                                           101
cps19_fed_gov_sat How satisfied are you with the performance of the federal government
under Justin Trudeau?

   o Very satisfied (1)
   o Fairly satisfied (2)
   o Not very satisfied (3)
   o Not at all satisfied (4)
   o Don't know/ Prefer not to answer (5)
cps19_fed_gov_sat Quel est votre niveau de satisfaction de la performance du gouvernement
fédéral sous Justin Trudeau?

   o Très satisfait (1)
   o Assez satisfait (2)
   o Pas très satisfait (3)
   o Pas du tout satisfait (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
Page Break




                                                                                         102
cps19_party_rating How do you feel about the federal political parties below? Set the slider to a
number from 0 to 100, where 0 means you really dislike the party and 100 means you really
like the party.

If you do not know, or prefer not to answer, please click →
                                                  Really dislike   Really like    Don't know/
                                                                                  Prefer not to
                                                                                    answer

                                                   0   10 20 30 40 50 60 70 80 90 100

                                Liberal Party ()

                         Conservative Party ()

                                        NDP ()

                             Bloc Québécois ()

                                Green Party ()

                              People's Party ()




cps19_party_rating Que pensez-vous des partis fédéraux énumérés ci-dessous? Veuillez
glisser la barre sur un chiffre entre 0 et 100, où 0 indique que vous n'aimez vraiment pas du
tout ce parti et 100 que vous aimez vraiment beaucoup ce parti.

Si vous ne savez pas, ou préférez ne pas répondre, veuillez appuyer sur →
                                                 Je n'aime     J'aime vraiment Je ne sais
                                              vraiment pas du beaucoup        pas/préfère ne
                                                    tout                       pas répondre

                                                   0   10 20 30 40 50 60 70 80 90 100




                                                                                             103
                    Parti libéral ()

             Parti conservateur ()

                           NPD ()

                Bloc québécois ()

                      Parti vert ()

                Parti populaire ()




Page Break




                                       104
cps19_lead_rating How do you feel about the federal party leaders below? Set the slider to a
number from 0 to 100, where 0 means you really dislike the leader and 100 means you really
like the leader.

If you do not know, or prefer not to answer, please click →
                                                  Really dislike    Really like    Don't know/
                                                                                   Prefer not to
                                                                                     answer

                                                  0   10 20 30 40 50 60 70 80 90 100

                              Justin Trudeau ()

                             Andrew Scheer ()

                             Jagmeet Singh ()

                    Yves-François Blanchet ()

                              Elizabeth May ()

                             Maxime Bernier ()




cps19_lead_rating Que pensez-vous des chefs de partis fédéraux énumérés ci-dessous?
Veuillez glisser la barre sur un chiffre entre 0 et 100, où 0 indique que vous n'aimez vraiment
pas du tout ce chef et 100 que vous aimez vraiment beaucoup ce chef.


Si vous ne savez pas, ou préférez ne pas répondre, veuillez appuyer sur →
                                                 Je n'aime     J'aime vraiment Je ne sais
                                              vraiment pas du beaucoup        pas/préfère ne
                                                    tout                       pas répondre

                                                  0   10 20 30 40 50 60 70 80 90 100




                                                                                              105
                     Justin Trudeau ()

                     Andrew Scheer ()

                     Jagmeet Singh ()

             Yves-François Blanchet ()

                      Elizabeth May ()

                    Maxime Bernier ()




Page Break




                                         106
cps19_cand_rating How do you feel about the candidates in your local riding? Set the slider
to a number from 0 to 100, where 0 means you really dislike the candidate and 100 means you
really like the candidate.

If you do not know, or prefer not to answer, please click →
                                                  Really dislike    Really like    Don't know/
                                                                                   Prefer not to
                                                                                     answer

                                                    0   10 20 30 40 50 60 70 80 90 100

             Liberal candidate in your riding ()

       Conservative candidate in your riding ()

               NDP candidate in your riding ()

    Bloc Québécois candidate in your riding ()

              Green candidate in your riding ()

     People's Party candidate in your riding ()




cps19_cand_rating Que pensez-vous des candidat(e)s dans votre circonscription locale?
Veuillez glisser la barre sur un chiffre entre 0 et 100, où 0 indique que vous n'aimez vraiment
pas du tout ce chef et 100 que vous aimez vraiment beaucoup ce chef.


Si vous ne savez pas, ou préférez ne pas répondre, veuillez appuyer sur →


                                                      Je n'aime   J'aime vraiment Je ne sais
                                                   vraiment pas du beaucoup      pas/préfère ne
                                                         tout                     pas répondre

                                                    0   10 20 30 40 50 60 70 80 90 100




                                                                                              107
               Candidat(e) libéral(e) dans votre
                               circonscription ()
     Candidat(e) conservateur/trice dans votre
                            circonscription ()
                 Candidat(e) du NPD dans votre
                               circonscription ()
    Candidat(e) du Bloc québécois dans votre
                            circonscription ()
 Candidat(e) vert(e) dans votre circonscription
                                              ()
     Candidat(e) du Parti populaire dans votre
                             circonscription ()



End of Block: Democracy, voting, and parties



   8.3.3        Ideology

NOTE: Respondents were randomly assigned to receive either
cps19_lr_scale_bef or cps19_lr_scale_aft, as part of an experiment on
ordering effects. If the embedded data field lr_scale_order was equal
to "individual_first", they received the individual self-placement
question cps19_lr_scale_bef, and then the party placement question
cps19_lr_parties. If the embedded data field lr_scale_order was equal
to "party_first", they received the the party placement question
cps19_lr_parties, and then the individual self-placement question
cps19_lr_scale_aft.


Start of Block: Ideology - left-right scales




Display This Question:
    If lr_scale_order = individual_first


cps19_lr_scale_bef In politics, people sometimes talk of left and right. Where would you place
yourself on this scale?




                                                                                            108
If you do not know, or prefer not to answer, please click →
                                                        Left               Right           Don't know/
                                                                                           Prefer not to
                                                                                             answer

                                                   0   1       2   3   4    5      6   7     8    9   10

                                       &nbsp ()




cps19_lr_scale_bef En politique, on parle parfois de gauche et de droite. Où vous placeriez-
vous sur cette échelle?




Si vous ne savez pas, ou préférez ne pas répondre, veuillez appuyer sur →
                                                  Gauche           Droite                Je ne sais
                                                                                       pas/Préfère ne
                                                                                        pas répondre

                                                   0   1       2   3   4    5      6   7     8    9   10

                                       &nbsp ()




Page Break




                                                                                                      109
cps19_lr_parties In politics, people sometimes talk of left and right. Where would you place the
federal political parties on a scale from 0 to 10 where 0 means the left and 10 means the right?

If you do not know, or prefer not to answer, please click →
                                                        Left               Right           Don't know/
                                                                                           Prefer not to
                                                                                             answer

                                                   0   1       2   3   4    5      6   7     8    9   10

                                Liberal Party ()

                          Conservative Party ()

                                        NDP ()

                             Bloc Québécois ()

                                 Green Party ()

                              People's Party ()




cps19_lr_parties
En politique, on parle parfois de gauche et de droite. Où placeriez-vous les partis politiques
fédéraux sur une échelle de 0 à 10, où 0 indique la gauche et 10 la droite?


Si vous ne savez pas, ou préférez ne pas répondre, veuillez appuyer sur →
                                                  Gauche           Droite                Je ne sais
                                                                                       pas/Préfère ne
                                                                                        pas répondre

                                                   0   1       2   3   4    5      6   7     8    9   10




                                                                                                      110
                    Parti libéral ()

             Parti conservateur ()

                           NPD ()

                Bloc québécois ()

                      Parti vert ()

                Parti populaire ()




Page Break




                                       111
Display This Question:
    If lr_scale_order = party_first


cps19_lr_scale_aft In politics, people sometimes talk of left and right. Where would you place
yourself on this scale?

If you do not know, or prefer not to answer, please click →
                                                        Left               Right           Don't know/
                                                                                           Prefer not to
                                                                                             answer

                                                   0   1       2   3   4    5      6   7     8    9   10

                                       &nbsp ()




cps19_lr_scale_aft En politique, on parle parfois de gauche et de droite. Où vous placeriez-
vous sur cette échelle?


Si vous ne savez pas, ou préférez ne pas répondre, veuillez appuyer sur →
                                                  Gauche           Droite                Je ne sais
                                                                                       pas/Préfère ne
                                                                                        pas répondre

                                                   0   1       2   3   4    5      6   7     8    9   10

                                       &nbsp ()




End of Block: Ideology - left-right scales



   8.3.4        Leader impressions


Start of Block: Leader impressions




                                                                                                      112
cps19_lead_int Which party leader(s) below do you think is/are intelligent? (Select all that
apply)


   ▢           Justin Trudeau (113)


   ▢           Andrew Scheer (114)


   ▢           Jagmeet Singh (115)


   ▢           Yves-François Blanchet (116)


   ▢           Elizabeth May (117)


   ▢           Maxime Bernier (118)


   ▢           ⊗None of these (119)

   ▢           ⊗Don't know/ Prefer not to answer (120)




                                                                                               113
cps19_lead_int Parmi les chefs de partis fédéraux énumérés ci-dessous, le(s)quel(s) trouvez-
vous intelligent(s)? (Sélectionnez tous ceux qui s'appliquent)


   ▢          Justin Trudeau (113)


   ▢          Andrew Scheer (114)


   ▢          Jagmeet Singh (115)


   ▢          Yves-François Blanchet (116)


   ▢          Elizabeth May (117)


   ▢          Maxime Bernier (118)


   ▢          ⊗Aucun de ces chefs (119)

   ▢          ⊗Je ne sais pas/Préfère ne pas répondre (120)

Page Break




                                                                                          114
Carry Forward All Choices - Displayed & Hidden from "Which party leader(s) below do you think
is/are intelligent? (Select all that apply)"




cps19_lead_strong Which party leader(s) below do you think provide(s) strong leadership?
(Select all that apply)


   ▢           Justin Trudeau (1)


   ▢           Andrew Scheer (2)


   ▢           Jagmeet Singh (3)


   ▢           Yves-François Blanchet (4)


   ▢           Elizabeth May (5)


   ▢           Maxime Bernier (6)


   ▢           ⊗None of these (7)

   ▢           ⊗Don't know/ Prefer not to answer (8)




                                                                                                115
cps19_lead_strong Parmi les chefs de partis fédéraux ci-dessous, le(s)quel(s) manifeste(nt)
un leadership fort ? (Sélectionnez tous ceux qui s'appliquent)


   ▢          Justin Trudeau (1)


   ▢          Andrew Scheer (2)


   ▢          Jagmeet Singh (3)


   ▢          Yves-François Blanchet (4)


   ▢          Elizabeth May (5)


   ▢          Maxime Bernier (6)


   ▢          ⊗Aucun de ces chefs (7)

   ▢          ⊗Je ne sais pas/Préfère ne pas répondre (8)

Page Break




                                                                                              116
Carry Forward All Choices - Displayed & Hidden from "Which party leader(s) below do you think
is/are intelligent? (Select all that apply)"




cps19_lead_trust Which party leader(s) below do you think is/are trustworthy? (Select all that
apply)


   ▢           Justin Trudeau (1)


   ▢           Andrew Scheer (2)


   ▢           Jagmeet Singh (3)


   ▢           Yves-François Blanchet (4)


   ▢           Elizabeth May (5)


   ▢           Maxime Bernier (6)


   ▢           ⊗None of these (7)

   ▢           ⊗Don't know/ Prefer not to answer (8)




                                                                                                117
cps19_lead_trust Parmi les chefs de partis fédéraux énumérés ci-dessous, le(s)quel(s) trouvez-
vous digne(s) de confiance? (Sélectionnez tous ceux qui s'appliquent)


   ▢          Justin Trudeau (1)


   ▢          Andrew Scheer (2)


   ▢          Jagmeet Singh (3)


   ▢          Yves-François Blanchet (4)


   ▢          Elizabeth May (5)


   ▢          Maxime Bernier (6)


   ▢          ⊗Aucun de ces chefs (7)

   ▢          ⊗Je ne sais pas/Préfère ne pas répondre (8)

Page Break




                                                                                          118
Carry Forward All Choices - Displayed & Hidden from "Which party leader(s) below do you think
is/are intelligent? (Select all that apply)"




cps19_lead_cares Which party leader(s) below do you think really care(s) about people like
you? (Select all that apply)


   ▢           Justin Trudeau (1)


   ▢           Andrew Scheer (2)


   ▢           Jagmeet Singh (3)


   ▢           Yves-François Blanchet (4)


   ▢           Elizabeth May (5)


   ▢           Maxime Bernier (6)


   ▢           ⊗None of these (7)

   ▢           ⊗Don't know/ Prefer not to answer (8)




                                                                                                119
cps19_lead_cares Parmi les chefs de partis fédéraux énumérés ci-dessous, le(s)quel(s) se
souci(ent) vraiment des gens comme vous? (Sélectionnez tous ceux qui s'appliquent)


   ▢          Justin Trudeau (1)


   ▢          Andrew Scheer (2)


   ▢          Jagmeet Singh (3)


   ▢          Yves-François Blanchet (4)


   ▢          Elizabeth May (5)


   ▢          Maxime Bernier (6)


   ▢          ⊗Aucun de ces chefs (7)

   ▢          ⊗Je ne sais pas/Préfère ne pas répondre (8)
End of Block: Leader impressions



   8.3.5      Government spending


Note: The order of the 5 government spending questions was randomized.


Start of Block: Government spending - education




                                                                                           120
cps19_spend_educ How much should the federal government spend on education?

   o Spend less (1)
   o Spend about the same as now (2)
   o Spend more (3)
   o Don't know/ Prefer not to answer (4)
cps19_spend_educ Combien le gouvernement fédéral devrait-il dépenser en éducation?

   o Dépenser moins (1)
   o Dépenser à peu près autant (2)
   o Dépenser plus (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
End of Block: Government spending - education

Start of Block: Government spending - environment




cps19_spend_env How much should the federal government spend on the environment?

   o Spend less (1)
   o Spend about the same as now (2)
   o Spend more (3)
   o Don't know/ Prefer not to answer (4)



                                                                                     121
cps19_spend_env Combien le gouvernement fédéral devrait-il dépenser en environnement?

   o Dépenser moins (1)
   o Dépenser à peu près autant (2)
   o Dépenser plus (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
End of Block: Government spending - environment

Start of Block: Government spending - justice_law




cps19_spend_just_law How much should the federal government spend on
${e://Field/justice_law}?

   o Spend less (1)
   o Spend about the same as now (2)
   o Spend more (3)
   o Don't know/ Prefer not to answer (4)
cps19_spend_just_law Combien le gouvernement fédéral devrait-il dépenser
pour ${e://Field/justice_law_fr}?

   o Dépenser moins (1)
   o Dépenser à peu près autant (2)
   o Dépenser plus (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
End of Block: Government spending - justice_law




                                                                                    122
Start of Block: Government spending - defence




cps19_spend_defence How much should the federal government spend on defence?

   o Spend less (1)
   o Spend about the same as now (2)
   o Spend more (3)
   o Don't know/ Prefer not to answer (4)
cps19_spend_defence
Combien le gouvernement fédéral devrait-il dépenser en défense?

   o Dépenser moins (1)
   o Dépenser à peu près autant (2)
   o Dépenser plus (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
End of Block: Government spending - defence

Start of Block: Government spending - immigrants and minorities




                                                                               123
cps19_spend_imm_min How much should the federal government spend on immigrants and
minorities?

   o Spend less (1)
   o Spend about the same as now (2)
   o Spend more (3)
   o Don't know/ Prefer not to answer (4)
cps19_spend_imm_min
Combien le gouvernement fédéral devrait-il dépenser pour les immigrants et les minorités?

   o Dépenser moins (1)
   o Dépenser à peu près autant (2)
   o Dépenser plus (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
End of Block: Government spending - immigrants and minorities



   8.3.6      Issue positions


Note: To leave more room for other questions, respondents only
received 3 out of the 9 issue positions, selected randomly. The order
they were presented in was also randomized.


Start of Block: Issue positions - intro




cps19_pos_intro Now we will ask your opinion about a number of political issues. For each one,
please tell us whether you strongly disagree, somewhat disagree, neither agree nor disagree,
somewhat agree or strongly agree.




                                                                                          124
cps19_pos_intro Nous allons maintenant vous demander votre avis sur un certain nombre
d'enjeux politiques. Pour chaque enjeu, veuillez nous indiquer si vous êtes fortement en
désaccord, plutôt en désaccord, ni en accord, ni en désaccord, plutôt d'accord ou fortement
d'accord.


End of Block: Issue positions - intro

Start of Block: Issue positions - electoral reform




cps19_pos_fptp Canada should change its electoral system from “First Past the Post” to a
“proportional representation” system.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                              125
cps19_pos_fptp
Le Canada devrait changer son système électoral afin de passer du mode de scrutin actuel à un
système de "représentation proportionnelle".

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Issue positions - electoral reform

Start of Block: Issue positions - assisted dying




cps19_pos_life Individuals who are terminally ill should be allowed to end their lives with the
assistance of a doctor.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)



                                                                                              126
cps19_pos_life Les individus en phase terminale devraient pouvoir mettre fin à leurs jours avec
l'aide d'un médecin.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Issue positions - assisted dying

Start of Block: Issue positions - cannabis




cps19_pos_cannabis Possession of cannabis should be a criminal offence.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                            127
cps19_pos_cannabis La possession de cannabis devrait être une infraction pénale.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Issue positions - cannabis

Start of Block: Issue positions - carbon tax




cps19_pos_carbon To help reduce greenhouse gas emissions, the federal government should
continue the carbon tax.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                    128
cps19_pos_carbon Afin d'aider à réduire les émissions de gaz à effet de serre, le gouvernement
fédéral devrait maintenir la taxe sur le carbone.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Issue positions - carbon tax

Start of Block: Issue positions - pipelines




cps19_pos_energy The federal government should do more to help Canada’s energy sector,
including building oil pipelines.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)



                                                                                          129
cps19_pos_energy Le gouvernement fédéral devrait en faire davantage afin d'aider le secteur
énergétique canadien, notamment en construisant des oléoducs.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Issue positions - pipelines

Start of Block: Issue positions - environmental regulation




cps19_pos_envreg Environmental regulation should be stricter, even if it leads to consumers
having to pay higher prices.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)



                                                                                         130
cps19_pos_envreg La réglementation environnementale devrait être plus stricte, même si elle
oblige les consommateurs à payer des prix plus élevés.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Issue positions - environmental regulation

Start of Block: Issue positions - environment versus jobs




cps19_pos_jobs When there is a conflict between protecting the environment and creating
jobs, jobs should come first.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)



                                                                                          131
cps19_pos_jobs Lorsqu'il existe un conflit entre la protection de l'environnement et la création
d'emplois, les emplois devraient avoir la priorité.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Issue positions - environment versus jobs

Start of Block: Issue positions - subsidies




cps19_pos_subsid The federal government should end all corporate and economic
development subsidies.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)



                                                                                              132
cps19_pos_subsid Le gouvernement fédéral devrait mettre fin à toutes les subventions au
développement des entreprises et de l'économie.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Issue positions - subsidies

Start of Block: Issue positions - free trade




cps19_pos_trade There should be more free trade with other countries, even if it hurts some
industries in Canada.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)



                                                                                          133
cps19_pos_trade Il devrait y avoir plus de libre-échange avec d'autres pays, même si cela nuit
à certaines industries au Canada.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Issue positions - free trade



   8.3.7      The economy


Start of Block: The economy




cps19_econ_retro Over the past year, has Canada's economy:

   o Got better (1)
   o Stayed about the same (2)
   o Got worse (3)
   o Don’t know/ Prefer not to answer (4)




                                                                                            134
cps19_econ_retro Depuis un an, l'économie canadienne s'est-elle:

   o Améliorée (1)
   o Restée à peu près la même (2)
   o Détériorée (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
Page Break




                                                                   135
cps19_econ_fed Have the policies of the federal government made Canada's economy...

   o Better (1)
   o Worse (2)
   o Not made much difference (3)
   o Don't know/ Prefer not to answer (4)
cps19_econ_fed
Les politiques du gouvernement fédéral ont contribué à...



   o Améliorer l'économie canadienne (1)
   o Détériorer l'économie canadienne (2)
   o N'ont pas changé grand chose à l'économie canadienne (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
Page Break




                                                                                      136
cps19_ownfinanc_fed Have the policies of the federal government made your financial
situation...

   o Better (1)
   o Worse (2)
   o Not made much difference (3)
   o Don't know/ Prefer not to answer (4)
cps19_ownfinanc_fed
Les politiques du gouvernement fédéral ont contribué à...



   o Améliorer votre situation financière (1)
   o Détériorer votre situation financière (2)
   o Pas changé grand chose à votre situation financière (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
End of Block: The economy



   8.3.8      Party issue handling

NOTE: cps19_issue_handle was set to receive a split sample of 50%
(1/2), to make room in the survey for more questions. Whether a
respondent was assigned to receive cps19_issue_handle was randomly
determined in the Survey Flow by setting the embedded data field
get_party_issue_handling to either 0 or 1. If get_party_issue_handling
was equal to 1, they were assigned to receive cps19_issue_handle.
get_party_issue_handling can be used to filter the dataset to only
respondents that were assigned to receive cps19_issue_handle.


Start of Block: Party issue handling


                                                                                      137
cps19_issue_handle Which party would do the best job at handling each of the following
issues?
                                                                                      Don't
                                                                                      know/
                 Liberal                            Bloc        Green
                           Conservative   NDP                            People's    Prefer
                  Party                           Québécois     Party
                             Party (2)     (3)                           Party (6)    not to
                   (1)                               (4)         (5)
                                                                                     answer
                                                                                       (7)

  Healthcare
     (1)            o           o           o          o           o         o           o
  Education
     (2)            o           o           o          o           o         o           o
 Environment
      (3)           o           o           o          o           o         o           o
  Crime and
  Justice (4)       o           o           o          o           o         o           o
 Defence (5)
                    o           o           o          o           o         o           o
 International
  diplomacy
      (6)           o           o           o          o           o         o           o
 Immigration
    and
  minorities
     (7)
                    o           o           o          o           o         o           o
  Economy
     (8)            o           o           o          o           o         o           o




                                                                                          138
cps19_issue_handle
Quel parti aborderait le mieux chacun de ces enjeux?
                                                                                     Je ne sais
                      Parti       Parti                Bloc      Part     Parti     pas/Préfère
                                              NPD
                     libéral   conservateur          québécois   vert   populaire     ne pas
                                               (3)
                        (1)        (2)                  (4)      (5)       (6)       répondre
                                                                                         (7)

   Les soins de
     santé (1)           o          o           o        o          o       o            o
  L'éducation (2)
                         o          o           o        o          o       o            o
 L'environnement
        (3)              o          o           o        o          o       o            o
  Le crime et la
   justice (4)           o          o           o        o          o       o            o
  La défense (5)
                         o          o           o        o          o       o            o
  La diplomatie
  internationale
        (6)              o          o           o        o          o o                  o
 L'immigration et
 les minorités (7)       o          o           o        o          o o                  o
  L'économie (8)
                         o          o           o        o          o o                  o

End of Block: Party issue handling



   8.3.9       Party chances


Start of Block: Party chances




                                                                                             139
cps19_most_seats For each of the parties below, how likely is each party to win the most seats
in the House of Commons?

If you do not know, or prefer not to answer, please click →
                                                  No chance at    Absolutely      Don’t know/
                                                  all of winning certain to win   Prefer not to
                                                 the most seats the most seats      answer

                                                  0   10 20 30 40 50 60 70 80 90 100

                               Liberal Party ()

                         Conservative Party ()

                                       NDP ()

                           Bloc Québécois ()

                                Green Party ()

                             People’s Party ()




cps19_most_seats
Quel parti a le plus de chances de gagner le plus grand nombre de sièges à la Chambre des
communes?


Si vous ne savez pas, ou préférez ne pas répondre, veuillez sélectionner →
                                              Aucune chance Absolument           Je ne sais
                                               de gagner le        certain de  pas/Préfère ne
                                                plus grand      gagner le plus pas répondre
                                                nombre de       grand nombre
                                                   sièges          de sièges

                                                  0   10 20 30 40 50 60 70 80 90 100




                                                                                            140
                    Parti libéral ()

             Parti conservateur ()

                           NPD ()

                Bloc québécois ()

                      Parti vert ()

                Parti populaire ()




Page Break




                                       141
cps19_win_local For each of the parties below, how likely is each party to win the seat in your
own local riding?

If you do not know, or prefer not to answer, please click →
                                                  No chance at      Absolutely      Don’t know/
                                                  all of winning   certain to win   Prefer not to
                                                   your riding      your riding       answer

                                                   0   10 20 30 40 50 60 70 80 90 100

                                Liberal Party ()

                         Conservative Party ()

                                        NDP ()

                            Bloc Québécois ()

                                Green Party ()

                              People’s Party ()




cps19_win_local
Quel parti a le plus de chances de gagner le siège dans votre circonscription?


Si vous ne savez pas, ou préférez ne pas répondre, veuillez sélectionner →
                                              Aucune chance Absolument           Je ne sais
                                               de gagner le        certain de  pas/Préfère ne
                                                   siège       gagner le siège pas répondre

                                                   0   10 20 30 40 50 60 70 80 90 100




                                                                                              142
                              Parti libéral ()

                       Parti conservateur ()

                                       NPD ()

                          Bloc québécois ()

                                   Parti vert ()

                           Parti populaire ()




End of Block: Party chances



   8.3.10    Election outcomes

NOTE: cps19_outcome_most and cps19_outcome_least were set to receive a
split sample of 50% (1/2), to make room in the survey for more
questions. Whether a respondent was assigned to receive
cps19_outcome_most and cps19_outcome_least was randomly determined in
the Survey Flow by setting the embedded data field get_outcome to
either 0 or 1. If get_outcome was equal to 1, they were assigned to
receive cps19_outcome_most and cps19_outcome_least. get_outcome can
be used to filter the dataset to only respondents that were assigned
to receive cps19_outcome_most and cps19_outcome_least.


Start of Block: Election outcome




                                                                    143
cps19_outcome_most Which election outcome would you most prefer?

   o Liberal majority (8)
   o Conservative majority (9)
   o NDP majority (10)
   o Liberal minority (11)
   o Conservative minority (12)
   o NDP minority (13)
   o Other government (14) ________________________________________________
   o Don't know/ Prefer not to answer (15)
cps19_outcome_most Quel résultat électoral préféreriez-vous le plus?

   o Majorité libérale (8)
   o Majorité conservatrice (9)
   o Majorité NPD (10)
   o Minorité libérale (11)
   o Minorité conservatrice (12)
   o Minorité NPD (13)
   o Autre gouvernement (14) ________________________________________________
   o Je ne sais pas/Préfère ne pas répondre (15)
Page Break




                                                                              144
cps19_outcome_least Which election outcome would you least prefer?
Which election outcome would you most prefer? != Liberal majority

   o Liberal majority (8)
Which election outcome would you most prefer? != Conservative majority

   o Conservative majority (9)
Which election outcome would you most prefer? != NDP majority

   o NDP majority (10)
Which election outcome would you most prefer? != Liberal minority

   o Liberal minority (11)
Which election outcome would you most prefer? != Conservative minority

   o Conservative minority (12)
Which election outcome would you most prefer? != NDP minority

   o NDP minority (13)
   o Other government (14) ________________________________________________
   o Don't know/ Prefer not to answer (15)




                                                                              145
cps19_outcome_least Quel résultat d'élection aimeriez-vous le moins?
Which election outcome would you most prefer? != Liberal majority

   o Majorité libérale (8)
Which election outcome would you most prefer? != Conservative majority

   o Majorité conservatrice (9)
Which election outcome would you most prefer? != NDP majority

   o Majorité NPD (10)
Which election outcome would you most prefer? != Liberal minority

   o Minorité libérale (11)
Which election outcome would you most prefer? != Conservative minority

   o Minorité conservatrice (12)
Which election outcome would you most prefer? != NDP minority

   o Minorité NPD (13)
   o Autre gouvernement (14) ________________________________________________
   o Je ne sais pas/Préfère ne pas répondre (15)
End of Block: Election outcome



   8.3.11      Immigration and refugees


NOTE: The order of cps19_imm and cps19_refugees was randomized.


Start of Block: Immigration




                                                                           146
cps19_imm Do you think Canada should admit:

   o More immigrants (1)
   o Fewer immigrants (2)
   o About the same number of immigrants as now (3)
   o Don’t know/ Prefer not to answer (4)
cps19_imm Pensez-vous que le Canada devrait admettre:

   o Plus d'immigrants (1)
   o Moins d'immigrants (2)
   o À peu près le même nombre d'immigrants (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
Page Break




                                                        147
End of Block: Immigration

Start of Block: Refugees




cps19_refugees Do you think Canada should admit:

   o More refugees (1)
   o Fewer refugees (2)
   o About the same number of refugees as now (3)
   o Don’t know/ Prefer not to answer (4)
cps19_refugees Pensez-vous que le Canada devrait admettre:

   o Plus de réfugiés (1)
   o Moins de réfugiés (2)
   o À peu près le même nombre de réfugiés (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
End of Block: Refugees



   8.3.12     Efficacy

NOTE: The order of the three efficacy questions, cps19_govt_confusing,
cps19_govt_say, and cps19_pol_eth, were randomized.


Start of Block: Efficacy intro




                                                                    148
cps19_eff_intro Now we will ask your opinion about a few more political issues. For each one,
please tell us whether you strongly disagree, somewhat disagree, somewhat agree or strongly
agree.

cps19_eff_intro Nous allons maintenant vous demander votre avis sur un certain nombre
d'autres enjeux politiques. Pour chaque énoncé, veuillez nous indiquer si vous êtes fortement
en désaccord, plutôt en désaccord, plutôt d'accord ou fortement d'accord.


End of Block: Efficacy intro

Start of Block: Efficacy - understand




cps19_govt_confusing Sometimes, politics and government seem so complicated that a person
like me can't really understand what's going on.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Somewhat agree (3)
   o Strongly agree (4)
   o Don't know/ Prefer not to answer (5)
cps19_govt_confusing
Parfois, la politique et le gouvernement semblent si compliqués qu'une personne comme moi ne
peut pas vraiment comprendre ce qui se passe.




                                                                                            149
   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Plutôt d'accord (3)
   o Fortement en accord (4)
   o Je ne sais pas/Préfère ne pas répondre (5)
End of Block: Efficacy - understand

Start of Block: Efficacy - say in government




cps19_govt_say People like me don't have any say about what the government does.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Somewhat agree (3)
   o Strongly agree (4)
   o Don't know/ Prefer not to answer (5)




                                                                                   150
cps19_govt_say
Les gens comme moi n'ont rien à dire sur ce que le gouvernement fait.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Plutôt d'accord (3)
   o Fortement d'accord (4)
   o Je ne sais pas/Préfère ne pas répondre (5)
End of Block: Efficacy - say in government

Start of Block: Efficacy - politician ethics




cps19_pol_eth It is important that politicians behave ethically in office.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Somewhat agree (3)
   o Strongly agree (4)
   o Don't know/ Prefer not to answer (5)




                                                                             151
cps19_pol_eth
Il est important que les politiciens se comportent de façon éthique dans l'exercice de leurs
fonctions.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Plutôt d'accord (3)
   o Fortement d'accord (4)
   o Je ne sais pas/Préfère ne pas répondre (5)
End of Block: Efficacy - politician ethics



   8.3.13      Election promises


Start of Block: Trudeau election promises




cps19_lib_promises Justin Trudeau kept the election promises he made in 2015.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Somewhat agree (3)
   o Strongly agree (4)
   o Don't know/ Prefer not to answer (5)



                                                                                               152
cps19_lib_promises
Justin Trudeau a tenu les promesses électorales qu'il avait faites en 2015.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Plutôt d'accord (3)
   o Tout à fait d'accord (4)
   o Je ne sais pas/Préfère ne pas répondre (5)
End of Block: Trudeau election promises



   8.3.14     SNC-Lavalin affair


Start of Block: SNC




cps19_snclav How would you rate how the government handled the SNC-Lavalin Affair? If you
haven’t heard about this, please indicate don’t know.

   o Very well (1)
   o Well (2)
   o Not very well (3)
   o Not at all well (4)
   o Don't know/ Prefer not to answer (5)



                                                                                       153
cps19_snclav Comment évalueriez-vous la manière dont le gouvernement a géré l'affaire SNC-
Lavalin? Si vous n'en avez pas entendu parler, veuillez sélectionner "je ne sais pas".

   o Très bien (1)
   o Bien (2)
   o Pas très bien (3)
   o Pas bien du tout (4)
   o Je ne sais pas/Préfère ne pas répondre (5)
End of Block: SNC




                                                                                       154
   8.3.15    News consumption


NOTE: cps19_news_cons was set to receive a split sample of 50% (1/2),
to make room in the survey for more questions. Whether a respondent
was assigned to receive cps19_news_cons was randomly determined in the
Survey Flow by setting the embedded data field get_news to either 0 or
1. If get_news was equal to 1, they were assigned to receive
cps19_news_cons. get_news can be used to filter the dataset to only
respondents that were assigned to receive cps19_news_cons.


Start of Block: News consumption




cps19_news_cons On average, how much time do you usually spend watching, reading, and
listening to news each day?

   o None (1)
   o 1-10 minutes (2)
   o 11-30 minutes (3)
   o 31-60 minutes (4)
   o Between 1 and 2 hours (5)
   o More than 2 hours (6)
   o Don't know/ Prefer not to answer (7)




                                                                                    155
cps19_news_cons En moyenne, combien de temps passez-vous chaque jour à lire, regarder et
écouter les nouvelles?

   o 0 minutes (1)
   o 1-10 minutes (2)
   o 11-30 minutes (3)
   o 31-60 minutes (4)
   o 1 à 2 heures (5)
   o Plus de 2 heures (6)
   o Je ne sais pas/Préfère ne pas répondre (7)
End of Block: News consumption




                                                                                     156
   8.3.16     Political participation


Start of Block: Political participation




cps19_volunteer In the past 12 months, how many times did you volunteer for a group or
organization such as a school, a religious organization, or sports or community associations?

   o Never (1)
   o Just once (2)
   o A few times (3)
   o More than five times (4)
   o Don't know/ Prefer not to answer (5)
cps19_volunteer Au cours des 12 derniers mois, combien de fois avez-vous fait du bénévolat
pour un groupe ou un organisme comme une école, une organisation religieuse ou une
association sportive ou communautaire?

   o Jamais (1)
   o Juste une fois (2)
   o Quelques fois (3)
   o Plus de cinq fois (4)
   o Je ne sais pas/Préfère ne pas répondre (5)
End of Block: Political participation



   8.3.17     Duty to vote


Start of Block: Duty to vote


                                                                                            157
cps19_duty_choice People have different views about voting. For some, voting is a duty. They
feel that they should vote in every election. For others, voting is a choice. They only vote when
they feel strongly about that election. For you personally, is voting first and foremost a Duty or
a Choice?

   o Duty (1)
   o Choice (2)
   o Don't know/ Prefer not to answer (3)
cps19_duty_choice Les gens ont des conceptions différentes du vote. Pour certains, voter est
un devoir. Ils croient qu'ils devraient voter à chaque élection. Pour d'autres, voter est un choix.
Ils votent seulement lorsqu'une élection les préoccupe vraiment. Pour vous personnellement,
est-ce que voter est un devoir ou un choix?

   o Devoir (1)
   o Choix (2)
   o Je ne sais pas/Préfère ne pas répondre (3)
End of Block: Duty to vote



   8.3.18      Quebec sovereignty


NOTE: This question was only displayed to respondents from Quebec.


Start of Block: Quebec sovereignty




                                                                                               158
cps19_quebec_sov Are you very favourable, somewhat favourable, somewhat opposed, or very
opposed to Quebec sovereignty, that is Quebec is no longer a part of Canada?

   o Very favourable (1)
   o Somewhat favourable (2)
   o Somewhat opposed (3)
   o Very opposed (4)
   o Don't know/ Prefer not to answer (5)
cps19_quebec_sov Êtes-vous très favorable, plutôt favorable, plutôt opposé(e) ou très
opposé(e) à la souveraineté du Québec, c'est-à-dire que le Québec ne fasse plus partie du
Canada?

   o Très favorable (1)
   o Plutôt favorable (2)
   o Plutôt opposé(e) (3)
   o Très opposé(e) (4)
   o Je ne sais pas/Préfère ne pas répondre (5)
End of Block: Quebec sovereignty




                                                                                        159
   8.3.19      Personal finances


Start of Block: Personal finances




cps19_own_fin_retro Over the past year, has your financial situation:

   o Got better (1)
   o Stayed about the same (2)
   o Got worse (3)
   o Don’t know/ Prefer not to answer (4)
cps19_own_fin_retro Pendant la dernière année, votre situation financière s'est-elle :

   o Améliorée (1)
   o Restée à peu près la même (2)
   o Détériorée (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
End of Block: Personal finances

   8.3.20      Political knowledge


NOTE: The 3rd and 4th questions in the section, cps19_govgen_name and
cps19_presrus_name, were set to be received by 50% (1/2) of the
respondents, to make room in the survey for more questions. Whether a
respondent was assigned to receive cps19_govgen_name and
cps19_presrus_name was randomly determined in the Survey Flow by
setting the embedded data field get_more_naming to either 0 or 1. If
get_more_naming was equal to 1, they were assigned to receive
cps19_govgen_name and cps19_presrus_name. get_more_naming can be used
to filter the dataset to only respondents that were assigned to
receive cps19_govgen_name and cps19_presrus_name.



                                                                                         160
Start of Block: Political knowledge




cps19_premier_name We would like to see how widely known some political figures are. Please
answer off the top of your head without checking online.

Do you happen to recall the name of the Premier of your Province?

If you do not know, or prefer not to answer, please click →

   ________________________________________________________________

cps19_premier_name Nous aimerions savoir à quel point certaines personnalités politiques sont
connues. Veuillez écrire la première réponse qui vous vient en tête sans vérifier en ligne.




Vous souvenez-vous du nom du premier ministre ou de la première ministre de votre
province?

Si vous ne savez pas, ou préférez ne pas répondre, veuillez cliquer sur la flèche →

   ________________________________________________________________



Page Break




                                                                                         161
cps19_finmin_name And the name of the federal Minister of Finance?

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

cps19_finmin_name Et le nom du/de la ministre fédéral(e) des finances?

Si vous ne savez pas, ou préférez ne pas répondre, veuillez cliquer sur la flèche →

    ________________________________________________________________



Page Break



Display This Question:
    If get_more_naming = 1


cps19_govgen_name And the name of the Governor-General of Canada?

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

cps19_govgen_name Et le nom du/de la gouverneur(e) général(e) du Canada?

Si vous ne savez pas, ou préférez ne pas répondre, veuillez cliquer sur la flèche →

    ________________________________________________________________



Page Break




                                                                                      162
Display This Question:
    If get_more_naming = 1


cps19_presrus_name And the name of the President of Russia?

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

cps19_presrus_name Et le nom du/de la président(e) de la Russie?

Si vous ne savez pas, ou préférez ne pas répondre, veuillez cliquer sur la flèche →

    ________________________________________________________________


End of Block: Political knowledge




                                                                                      163
   8.3.21     Premier satisfaction


NOTE: The name of the respondent’s premier, based on their province,
was piped into ${e://Field/premier} for this question.


Start of Block: Premier satisfaction




cps19_prov_gov_sat How satisfied are you with the performance of your provincial government
under ${e://Field/premier}?

   o Very satisfied (1)
   o Fairly satisfied (2)
   o Not very satisfied (3)
   o Not at all satisfied (4)
   o Don't know/ Prefer not to answer (5)
cps19_prov_gov_sat Quel est votre niveau de satisfaction de la performance du gouvernement
provincial sous ${e://Field/premier}?

   o Très satisfait (1)
   o Assez satisfait (2)
   o Pas très satisfait (3)
   o Pas du tout satisfait (4)
   o Je ne sais pas/Préfère ne pas répondre (5)
End of Block: Premier satisfaction




                                                                                        164
    8.3.22      Party identification and membership


Note: After they responded with their federal party identification,
the relevant party was piped into the relevant follow-up questions.


Start of Block: Party ID and membership part 1




cps19_fed_id In federal politics, do you usually think of yourself as a:

    o Liberal (1)
    o Conservative (2)
    o NDP (3)
Which province or territory are you currently living in? = Quebec

    o Bloc Québécois (4)
    o Green (5)
    o People’s Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o None of these (8)
    o Don't know/ Prefer not to answer (9)




                                                                           165
cps19_fed_id En politique fédérale, vous considérez-vous habituellement comme étant :

    o Libéral (1)
    o Conservateur (2)
    o NPD (3)
Which province or territory are you currently living in? = Quebec

    o Bloc québécois (4)
    o Parti vert (5)
    o Parti populaire du Canada (6)
    o Un autre parti (Veuillez spécifier) (7)
    ________________________________________________

    o Aucun de ces partis (8)
    o Je ne sais pas/Préfère ne pas répondre (9)
End of Block: Party ID and membership part 1

Start of Block: Party ID and membership part 2




Display This Question:
    If In federal politics, do you usually think of yourself as a: != None of these
    And In federal politics, do you usually think of yourself as a: != Don't know/ Prefer not to answer




                                                                                                          166
cps19_fed_id_str How strongly ${e://Field/pid_en}${cps19_fed_id/ChoiceTextEntryValue/7} do
you feel?

   o Very strongly (1)
   o Fairly strongly (2)
   o Not very strongly (3)
   o Don't know/ Prefer not to answer (4)
cps19_fed_id_str À quel point vous sentez-vous proche
du ${e://Field/pid_party_fr}${cps19_fed_id/ChoiceTextEntryValue/7}?

   o Très fortement (1)
   o Fortement (2)
   o Pas très fortement (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
Page Break




                                                                                        167
Display This Question:
    If Which province or territory are you currently living in? != Northwest Territories
    And Which province or territory are you currently living in? != Nunavut




                                                                                           168
cps19_prov_id In provincial politics, do you usually think of yourself as a:
Which province or territory are you currently living in? != Saskatchewan

    o Liberal (281)
Which province or territory are you currently living in? != Quebec
And Which province or territory are you currently living in? != Prince Edward Island

    o NDP (282)
Which province or territory are you currently living in? = British Columbia
Or Which province or territory are you currently living in? = Ontario
Or Which province or territory are you currently living in? = New Brunswick
Or Which province or territory are you currently living in? = Prince Edward Island

    o Green (283)
Which province or territory are you currently living in? = Quebec

    o Coalition Avenir Québec (284)
Which province or territory are you currently living in? = Quebec

    o Parti Québécois (285)
Which province or territory are you currently living in? = Quebec

    o Québec Solidaire (286)
Which province or territory are you currently living in? = Alberta

    o United Conservative (288)
Which province or territory are you currently living in? = Alberta

    o Alberta Party (289)
Which province or territory are you currently living in? = Alberta

    o Conservative (290)
Which province or territory are you currently living in? = Saskatchewan

    o Saskatchewan Party (291)
Which province or territory are you currently living in? = Nova Scotia
Or Which province or territory are you currently living in? = Newfoundland and Labrador
Or Which province or territory are you currently living in? = New Brunswick



                                                                                          169
Or Which province or territory are you currently living in? = Prince Edward Island
Or Which province or territory are you currently living in? = Ontario
Or Which province or territory are you currently living in? = Manitoba

    o Progressive Conservative (292)
Which province or territory are you currently living in? = New Brunswick

    o People's Alliance (298)
Which province or territory are you currently living in? = Yukon

    o Yukon Party (293)
    o Another party (please specify) (295)
    ________________________________________________

    o None of these (296)
    o Don't know/ Prefer not to answer (297)




                                                                                     170
cps19_prov_id En politique provinciale, vous considérez-vous habituellement comme étant:
Which province or territory are you currently living in? != Saskatchewan

    o Parti libéral (281)
Which province or territory are you currently living in? != Quebec
And Which province or territory are you currently living in? != Prince Edward Island

    o NPD (282)
Which province or territory are you currently living in? = British Columbia
Or Which province or territory are you currently living in? = Ontario
Or Which province or territory are you currently living in? = New Brunswick
Or Which province or territory are you currently living in? = Prince Edward Island

    o Parti vert (283)
Which province or territory are you currently living in? = Quebec

    o Coalition avenir Québec (284)
Which province or territory are you currently living in? = Quebec

    o Parti québécois (285)
Which province or territory are you currently living in? = Quebec

    o Québec solidaire (286)
Which province or territory are you currently living in? = Alberta

    o United Conservative (288)
Which province or territory are you currently living in? = Alberta

    o Alberta Party (289)
Which province or territory are you currently living in? = Alberta

    o Parti conservateur (290)
Which province or territory are you currently living in? = Saskatchewan

    o Saskatchewan Party (291)
Which province or territory are you currently living in? = Nova Scotia
Or Which province or territory are you currently living in? = Newfoundland and Labrador
Or Which province or territory are you currently living in? = New Brunswick



                                                                                          171
Or Which province or territory are you currently living in? = Prince Edward Island
Or Which province or territory are you currently living in? = Ontario
Or Which province or territory are you currently living in? = Manitoba

    o Parti progressiste-conservateur du Canada (292)
Which province or territory are you currently living in? = New Brunswick

    o Alliance des gens du Nouveau-Brunswick (298)
Which province or territory are you currently living in? = Yukon

    o Yukon Party (293)
    o Autre parti (veuillez spécifier) (295)
    ________________________________________________

    o Aucun de ces partis (296)
    o Je ne sais pas/Préfère ne pas répondre (297)
Page Break




                                                                                     172
Display This Question:
    If In provincial politics, do you usually think of yourself as a: != None of these
    And In provincial politics, do you usually think of yourself as a: != Don't know/ Prefer not to answer
And If
    Which province or territory are you currently living in? != Northwest Territories
    And Which province or territory are you currently living in? != Nunavut


cps19_prov_id_str How strongly ${cps19_prov_id/ChoiceGroup/SelectedChoicesTextEntry} do
you feel?

    o Very strongly (1)
    o Fairly strongly (2)
    o Not very strongly (3)
    o Don't know/ Prefer not to answer (4)
cps19_prov_id_str À quel point vous sentez-vous proche du
${cps19_prov_id/ChoiceGroup/SelectedChoicesTextEntry} ?

    o Très proche (1)
    o Assez proche (2)
    o Pas très proche (3)
    o Je ne sais pas/Préfère ne pas répondre (4)
Page Break




                                                                                                        173
cps19_party_member Are you currently… (Select all that apply)


   ▢          A dues-paying member of a federal political party (36)


   ▢          A dues-paying member of a provincial political party (37)


   ▢          A 'registered' supporter of the Liberal Party of Canada (38)


   ▢          ⊗None of the above (39)

   ▢          ⊗Don't know/ Prefer not to answer (40)
cps19_party_member Êtes-vous présentement… (Veuillez sélectionner toutes les options qui
s'appliquent)


   ▢          Un membre cotisant d'un parti politique fédéral (36)


   ▢          Un membre cotisant d'un parti politique provincial (37)


   ▢          Un partisan "inscrit" du Parti libéral du Canada (38)


   ▢          ⊗Aucune de ces options (39)

   ▢          ⊗Je ne sais pas/Préfère ne pas répondre (40)

Page Break




                                                                                       174
Display This Question:
     If Are you currently… (Select all that apply) = A dues-paying member of a <strong>federal
</strong>political party




cps19_fed_member Which federal party are you a dues-paying member of?

    o Liberal Party (56)
    o Conservative Party (57)
    o NDP (58)
    o Bloc Québécois (59)
    o Green Party (60)
    o People’s Party (61)
    o Other (please specify) (62) ________________________________________________
    o Don’t know/ Prefer not to answer (63)




                                                                                                 175
cps19_fed_member De quel parti fédéral êtes-vous membre cotisant?

   o Parti libéral (56)
   o Parti conservateur (57)
   o NPD (58)
   o Bloc québécois (59)
   o Parti vert (60)
   o Parti populaire (61)
   o Autre (Veuillez spécifier) (62)
   ________________________________________________

   o Je ne sais pas/Préfère ne pas répondre (63)
Page Break




                                                                    176
Display This Question:
    If Which province or territory are you currently living in? != Northwest Territories
    And Which province or territory are you currently living in? != Nunavut
And If
     Are you currently… (Select all that apply) = A dues-paying member of a <strong>provincial
</strong>political party




                                                                                                 177
cps19_prov_member Which provincial party are you a dues-paying member of?
Which province or territory are you currently living in? != Saskatchewan
And Which province or territory are you currently living in? != Manitoba

    o Liberal (281)
Which province or territory are you currently living in? != Quebec
And Which province or territory are you currently living in? != Prince Edward Island

    o NDP (282)
Which province or territory are you currently living in? = British Columbia
Or Which province or territory are you currently living in? = Ontario
Or Which province or territory are you currently living in? = Newfoundland and Labrador
Or Which province or territory are you currently living in? = Prince Edward Island

    o Green (283)
Which province or territory are you currently living in? = Quebec

    o Coalition Avenir Québec (284)
Which province or territory are you currently living in? = Quebec

    o Parti Québécois (285)
Which province or territory are you currently living in? = Quebec

    o Québec Solidaire (286)
Which province or territory are you currently living in? = Alberta

    o United Conservative (288)
Which province or territory are you currently living in? = Alberta

    o Alberta Party (289)
Which province or territory are you currently living in? = Alberta

    o Conservative (290)
Which province or territory are you currently living in? = Saskatchewan

    o Saskatchewan Party (291)
Which province or territory are you currently living in? = Nova Scotia
Or Which province or territory are you currently living in? = Newfoundland and Labrador



                                                                                          178
Or Which province or territory are you currently living in? = New Brunswick
Or Which province or territory are you currently living in? = Prince Edward Island
Or Which province or territory are you currently living in? = Ontario
Or Which province or territory are you currently living in? = Manitoba

    o Progressive Conservative (292)
Which province or territory are you currently living in? = New Brunswick

    o People's Alliance (298)
Which province or territory are you currently living in? = Yukon

    o Yukon Party (293)
    o Another party (please specify) (295)
    ________________________________________________

    o None of these (296)
    o Don't know/ Prefer not to answer (297)




                                                                                     179
cps19_prov_member De quel parti provincial êtes-vous membre cotisant?
Which province or territory are you currently living in? != Saskatchewan
And Which province or territory are you currently living in? != Manitoba

    o Libéral (281)
Which province or territory are you currently living in? != Quebec
And Which province or territory are you currently living in? != Prince Edward Island

    o NPD (282)
Which province or territory are you currently living in? = British Columbia
Or Which province or territory are you currently living in? = Ontario
Or Which province or territory are you currently living in? = Newfoundland and Labrador
Or Which province or territory are you currently living in? = Prince Edward Island

    o Parti vert (283)
Which province or territory are you currently living in? = Quebec

    o Coalition avenir Québec (284)
Which province or territory are you currently living in? = Quebec

    o Parti québécois (285)
Which province or territory are you currently living in? = Quebec

    o Québec solidaire (286)
Which province or territory are you currently living in? = Alberta

    o United Conservative (288)
Which province or territory are you currently living in? = Alberta

    o Alberta Party (289)
Which province or territory are you currently living in? = Alberta

    o Parti conservateur (290)
Which province or territory are you currently living in? = Saskatchewan

    o Saskatchewan Party (291)
Which province or territory are you currently living in? = Nova Scotia
Or Which province or territory are you currently living in? = Newfoundland and Labrador



                                                                                          180
Or Which province or territory are you currently living in? = New Brunswick
Or Which province or territory are you currently living in? = Prince Edward Island
Or Which province or territory are you currently living in? = Ontario
Or Which province or territory are you currently living in? = Manitoba

    o Progressive Conservative (292)
Which province or territory are you currently living in? = New Brunswick

    o People's Alliance (298)
Which province or territory are you currently living in? = Yukon

    o Yukon Party (293)
    o Autre (Veuillez spécifier) (295)
    ________________________________________________

    o Aucun de ces partis (296)
    o Je ne sais pas/Préfère ne pas répondre (297)
Page Break




                                                                                     181
cps19_fed_donate Since the 2015 federal election, have you donated money to any federal
political party or candidate, beyond buying a party membership?

 (This includes any national party, a local federal party association, a candidate in a federal
election, someone running to be a candidate in a federal election, or a candidate for the
leadership of a federal party).

   o Yes (1)
   o No (2)
   o Don't know/ Prefer not to answer (3)
cps19_fed_donate Depuis l'élection fédérale de 2015, avez-vous fait un don à un candidat ou
un parti politique fédéral, au-delà de l'achat d'une carte de membre?

(Ceci inclut tout parti national, une association de parti fédéral locale, un candidat lors d'une
élection fédérale, une personne se portant candidate à une élection fédérale ou un candidat à la
chefferie d'un parti fédéral.)

   o Oui (1)
   o Non (2)
   o Je ne sais pas/Préfère ne pas répondre (3)
End of Block: Party ID and membership part 2



   8.3.23      Groups thermometers


Start of Block: Groups thermometers




                                                                                                  182
cps19_groups_therm How do you feel about the following groups? Set the slider to any number
from 0 to 100, where 0 means you really dislike the group and 100 means you really like the
group.

If you do not know, or prefer not to answer, please click →
                                                  Really dislike   Really like   Don't know/
                                                                                 Prefer not to
                                                                                   answer

                                                    0   10 20 30 40 50 60 70 80 90 100

                            Racial minorities ()

                                  Immigrants ()

                              Francophones ()

                                    Feminists ()

                        Politicians in general ()




cps19_groups_therm Que pensez-vous des différents groupes ci-dessous? Veuillez glisser la
barre sur un chiffre entre 0 et 100, où 0 indique que vous n'aimez vraiment pas du tout un
groupe et 100 que vous aimez vraiment beaucoup un groupe.


Si vous ne savez pas, ou préférez ne pas répondre, veuillez sélectionner →
                                                 Je n'aime     J'aime vraiment Je ne sais
                                              vraiment pas du beaucoup        pas/préfère ne
                                                    tout                       pas répondre

                                                    0   10 20 30 40 50 60 70 80 90 100




                                                                                           183
                       Minorités raciales ()

                             Immigrants ()

                          Francophones ()

                              Féministes ()

                   Politiciens en général ()




End of Block: Groups thermometers




                                               184
   8.3.24      Past vote
Start of Block: Past vote




cps19_spoil Have you ever intentionally spoiled your ballot in an election (e.g. intentionally filled
out your ballot so your vote would not be counted for any candidate)?

   o Yes (1)
   o No (2)
   o Don't know/ Prefer not to answer (3)
cps19_spoil Avez-vous déjà intentionnellement annulé votre vote lors d'une élection (c'est-à-
dire que vous avez volontairement rempli votre bulletin de vote afin qu'il ne soit compté pour
aucun candidat)?

   o Oui (1)
   o Non (2)
   o Je ne sais pas / Préfère ne pas répondre (3)
Page Break




                                                                                                 185
Display This Question:
    If Are you a... = Canadian citizen


cps19_turnout_2015 Did you happen to vote in the last Federal election in 2015?

   o Yes (1)
   o No (2)
   o Not eligible to vote in last election (3)
   o Don't know/ Prefer not to answer (4)
cps19_turnout_2015 Avez-vous voté lors de la dernière élection fédérale en 2015?

   o Oui (1)
   o Non (2)
   o Pas éligible au vote lors de la dernière élection (3)
   o Je ne sais pas / Préfère ne pas répondre (4)
Page Break




                                                                                   186
Display This Question:
    If Did you happen to vote in the last Federal election in 2015? = Yes




cps19_vote_2015 Which party did you vote for in the Federal election in 2015?

   o Liberal Party (1)
   o Conservative Party (2)
   o NDP (3)
   o Bloc Québécois (4)
   o Green Party (5)
   o Another party (please specify) (6)
   ________________________________________________

   o Don't know/ Prefer not to answer (7)




                                                                                187
cps19_vote_2015 Pour quel parti avez-vous voté?

   o Parti libéral (1)
   o Parti conservateur (2)
   o NPD (3)
   o Bloc québécois (4)
   o Parti vert (5)
   o Un autre parti (Veuillez spécifier) (6)
   ________________________________________________

   o Je ne sais pas / Préfère ne pas répondre (7)
End of Block: Past vote




                                                      188
   8.3.25      Debates

NOTE: These two questions were set to automatically start being
displayed on the relevant day, in YYYYMMDD format.


Start of Block: Debates




Display This Question:
    If current_date > 20191007


cps19_debate_en Did you happen to watch or listen to the English-language federal leaders
debate on Monday, Oct. 7?

   o Yes (1)
   o No (2)
   o Don't know/ Prefer not to answer (3)
cps19_debate_en Avez-vous écouté ou regardé le débat des chefs fédéraux en anglais le lundi
7 octobre?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/Préfère ne pas répondre (3)
Page Break




                                                                                            189
Display This Question:
    If current_date > 20191010


cps19_debate_fr Did you happen to watch or listen to the French-language federal leaders
debate on Thursday, Oct. 10?

   o Yes (1)
   o No (2)
   o Don't know/ Prefer not to answer (3)
cps19_debate_fr Avez-vous écouté ou regardé le débat des chefs fédéraux en français le jeudi
10 octobre?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/Préfère ne pas répondre (3)
End of Block: Debates




                                                                                           190
   8.3.26    Additional demographics


Start of Block: Additional demographics




                                          191
cps19_religion Please tell me what is your religion, if you have one?

   o None/ Don't have one/ Atheist (1)
   o Agnostic (2)
   o Buddhist/ Buddhism (3)
   o Hindu (4)
   o Jewish/ Judaism/ Jewish Orthodox (5)
   o Muslim/ Islam (6)
   o Sikh/ Sikhism (7)
   o Anglican/ Church of England (8)
   o Baptist (9)
   o Catholic/ Roman Catholic/ RC (10)
   o Greek Orthodox/ Ukrainian Orthodox/ Russian Orthodox/ Eastern Orthodox (11)
   o Jehovah's Witness (12)
   o Lutheran (13)
   o Mormon/ Church of Jesus Christ of the Latter Day Saints (14)
   o Pentecostal/ Fundamentalist/ Born Again/ Evangelical (15)
   o Presbyterian (16)
   o Protestant (17)
   o United Church of Canada (18)
   o Christian Reformed (19)

                                                                                   192
o Salvation Army (20)
o Mennonite (21)
o Other (please specify) (22) ________________________________________________
o Don't know/ Prefer not to answer (23)




                                                                           193
cps19_religion Quelle est votre religion, si vous en avez une?

   o Aucune/ N'en a pas une / Athée (1)
   o Agnostique (2)
   o Bouddhiste / Bouddhisme (3)
   o Hindou (4)
   o Juif / Judaïsme / Orthodoxe Juif (5)
   o Musulman (6)
   o Sikh / Sikhisme (7)
   o Anglicane / Eglise d'Angleterre (8)
   o Baptiste (9)
   o Catholique / Catholique Romaine / RC (10)
   o Orthodoxe Grec / Orthodoxe Ukrainien / Orthodoxe Russe / Orthodoxe de l'Est (11)
   o Témoin de Jehovah (12)
   o Luthérien (13)
   o Mormon / Église de Jésus-Christ des Saints des Derniers Jours (14)
   o Pentecôtiste / Fondamentaliste / Né de nouveau / Évangélique (15)
   o Presbytérien (16)
   o Protestant (17)
   o Église Unie du Canada (18)
   o Réforme chrétienne (19)

                                                                                        194
  o Armée du Salut (20)
  o Mennonite (21)
  o Autre (Veuillez spécifier) (22)
  ________________________________________________

  o Je ne sais pas / Préfère ne pas répondre (23)
Page Break




                                                     195
Display This Question:
    If Please tell me what is your religion, if you have one? != None/ Don't have one/ Atheist


cps19_rel_imp In your life, you would say religion is:

   o Very important (1)
   o Somewhat important (2)
   o Not very important (3)
   o Not important at all (4)
   o Don't know/ Prefer not to answer (5)
cps19_rel_imp Dans votre vie, diriez-vous que la religion est:

   o Très importante (1)
   o Assez importante (2)
   o Pas très importante (3)
   o Pas importante du tout (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
Page Break




                                                                                                 196
cps19_bornin_canada Were you born in Canada?

   o Yes (1)
   o No (2)
   o Don’t know/ Prefer not to say (3)
cps19_bornin_canada Êtes-vous né au Canada?

   o Oui (1)
   o Non (2)
   o Je ne sais pas / Préfère ne pas répondre (3)
Page Break




                                                    197
Display This Question:
    If Were you born in Canada? = No




                                       198
cps19_bornin_other What country were you born in?

   o AFGHANISTAN (2243)
   o ÅLAND ISLANDS (2244)
   o ALBANIA (2245)
   o ALGERIA (2246)
   o AMERICAN SAMOA (2247)
   o ANDORRA (2248)
   o ANGOLA (2249)
   o ANGUILLA (2250)
   o ANTARCTICA (2251)
   o ANTIGUA AND BARBUDA (2252)
   o ARGENTINA (2253)
   o ARMENIA (2254)
   o ARUBA (2255)
   o AUSTRALIA (2256)
   o AUSTRIA (2257)
   o AZERBAIJAN (2258)
   o BAHAMAS (2259)
   o BAHRAIN (2260)
   o BANGLADESH (2261)

                                                    199
o BARBADOS (2262)
o BELARUS (2263)
o BELGIUM (2264)
o BELIZE (2265)
o BENIN (2266)
o BERMUDA (2267)
o BHUTAN (2268)
o BOLIVIA, PLURINATIONAL STATE OF (2269)
o BONAIRE, SINT EUSTATIUS AND SABA (2270)
o BOSNIA AND HERZEGOVINA (2271)
o BOTSWANA (2272)
o BOUVET ISLAND (2273)
o BRAZIL (2274)
o BRITISH INDIAN OCEAN TERRITORY (2275)
o BRUNEI DARUSSALAM (2276)
o BULGARIA (2277)
o BURKINA FASO (2278)
o BURUNDI (2279)
o CAMBODIA (2280)
o CAMEROON (2281)
                                            200
o CAPE VERDE (2282)
o CAYMAN ISLANDS (2283)
o CENTRAL AFRICAN REPUBLIC (2284)
o CHAD (2285)
o CHILE (2286)
o CHINA (2287)
o CHRISTMAS ISLAND (2288)
o COCOS (KEELING) ISLANDS (2289)
o COLOMBIA (2290)
o COMOROS (2291)
o CONGO (2292)
o CONGO, THE DEMOCRATIC REPUBLIC OF THE (2293)
o COOK ISLANDS (2294)
o COSTA RICA (2295)
o CÔTE D'IVOIRE (2296)
o CROATIA (2297)
o CUBA (2298)
o CURAÇAO (2299)
o CYPRUS (2300)
o CZECH REPUBLIC (2301)
                                                 201
o DENMARK (2302)
o DJIBOUTI (2303)
o DOMINICA (2304)
o DOMINICAN REPUBLIC (2305)
o ECUADOR (2306)
o EGYPT (2307)
o EL SALVADOR (2308)
o EQUATORIAL GUINEA (2309)
o ERITREA (2310)
o ESTONIA (2311)
o ETHIOPIA (2312)
o FALKLAND ISLANDS (MALVINAS) (2313)
o FAROE ISLANDS (2314)
o FIJI (2315)
o FINLAND (2316)
o FRANCE (2317)
o FRENCH GUIANA (2318)
o FRENCH POLYNESIA (2319)
o FRENCH SOUTHERN TERRITORIES (2320)
o GABON (2321)
                                       202
o GAMBIA (2322)
o GEORGIA (2323)
o GERMANY (2324)
o GHANA (2325)
o GIBRALTAR (2326)
o GREECE (2327)
o GREENLAND (2328)
o GRENADA (2329)
o GUADELOUPE (2330)
o GUAM (2331)
o GUATEMALA (2332)
o GUERNSEY (2333)
o GUINEA (2334)
o GUINEA-BISSAU (2335)
o GUYANA (2336)
o HAITI (2337)
o HEARD ISLAND AND MCDONALD ISLANDS (2338)
o HOLY SEE (VATICAN CITY STATE) (2339)
o HONDURAS (2340)
o HONG KONG (2341)
                                             203
o HUNGARY (2342)
o ICELAND (2343)
o INDIA (2344)
o INDONESIA (2345)
o IRAN, ISLAMIC REPUBLIC OF (2346)
o IRAQ (2347)
o IRELAND (2348)
o ISLE OF MAN (2349)
o ISRAEL (2350)
o ITALY (2351)
o JAMAICA (2352)
o JAPAN (2353)
o JERSEY (2354)
o JORDAN (2355)
o KAZAKHSTAN (2356)
o KENYA (2357)
o KIRIBATI (2358)
o KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF (2359)
o KOREA, REPUBLIC OF (2360)
o KUWAIT (2361)
                                                  204
o KYRGYZSTAN (2362)
o LAO PEOPLE'S DEMOCRATIC REPUBLIC (2363)
o LATVIA (2364)
o LEBANON (2365)
o LESOTHO (2366)
o LIBERIA (2367)
o LIBYA (2368)
o LIECHTENSTEIN (2369)
o LITHUANIA (2370)
o LUXEMBOURG (2371)
o MACAO (2372)
o MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF (2373)
o MADAGASCAR (2374)
o MALAWI (2375)
o MALAYSIA (2376)
o MALDIVES (2377)
o MALI (2378)
o MALTA (2379)
o MARSHALL ISLANDS (2380)
o MARTINIQUE (2381)
                                                      205
o MAURITANIA (2382)
o MAURITIUS (2383)
o MAYOTTE (2384)
o MEXICO (2385)
o MICRONESIA, FEDERATED STATES OF (2386)
o MOLDOVA, REPUBLIC OF (2387)
o MONACO (2388)
o MONGOLIA (2389)
o MONTENEGRO (2390)
o MONTSERRAT (2391)
o MOROCCO (2392)
o MOZAMBIQUE (2393)
o MYANMAR (2394)
o NAMIBIA (2395)
o NAURU (2396)
o NEPAL (2397)
o NETHERLANDS (2398)
o NEW CALEDONIA (2399)
o NEW ZEALAND (2400)
o NICARAGUA (2401)
                                           206
o NIGER (2402)
o NIGERIA (2403)
o NIUE (2404)
o NORFOLK ISLAND (2405)
o NORTHERN MARIANA ISLANDS (2406)
o NORWAY (2407)
o OMAN (2408)
o PAKISTAN (2409)
o PALAU (2410)
o PALESTINIAN TERRITORY, OCCUPIED (2411)
o PANAMA (2412)
o PAPUA NEW GUINEA (2413)
o PARAGUAY (2414)
o PERU (2415)
o PHILIPPINES (2416)
o PITCAIRN (2417)
o POLAND (2418)
o PORTUGAL (2419)
o PUERTO RICO (2420)
o QATAR (2421)
                                           207
o RÉUNION (2422)
o ROMANIA (2423)
o RUSSIAN FEDERATION (2424)
o RWANDA (2425)
o SAINT BARTHÉLEMY (2426)
o SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA (2427)
o SAINT KITTS AND NEVIS (2428)
o SAINT LUCIA (2429)
o SAINT MARTIN (FRENCH PART) (2430)
o SAINT PIERRE AND MIQUELON (2431)
o SAINT VINCENT AND THE GRENADINES (2432)
o SAMOA (2433)
o SAN MARINO (2434)
o SAO TOME AND PRINCIPE (2435)
o SAUDI ARABIA (2436)
o SENEGAL (2437)
o SERBIA (2438)
o SEYCHELLES (2439)
o SIERRA LEONE (2440)
o SINGAPORE (2441)
                                                        208
o SINT MAARTEN (DUTCH PART) (2442)
o SLOVAKIA (2443)
o SLOVENIA (2444)
o SOLOMON ISLANDS (2445)
o SOMALIA (2446)
o SOUTH AFRICA (2447)
o SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS (2448)
o SOUTH SUDAN (2449)
o SPAIN (2450)
o SRI LANKA (2451)
o SUDAN (2452)
o SURINAME (2453)
o SVALBARD AND JAN MAYEN (2454)
o SWAZILAND (2455)
o SWEDEN (2456)
o SWITZERLAND (2457)
o SYRIAN ARAB REPUBLIC (2458)
o TAIWAN, PROVINCE OF CHINA (2459)
o TAJIKISTAN (2460)
o TANZANIA, UNITED REPUBLIC OF (2461)
                                                        209
o THAILAND (2462)
o TIMOR-LESTE (2463)
o TOGO (2464)
o TOKELAU (2465)
o TONGA (2466)
o TRINIDAD AND TOBAGO (2467)
o TUNISIA (2468)
o TURKEY (2469)
o TURKMENISTAN (2470)
o TURKS AND CAICOS ISLANDS (2471)
o TUVALU (2472)
o UGANDA (2473)
o UKRAINE (2474)
o UNITED ARAB EMIRATES (2475)
o UNITED KINGDOM (2476)
o UNITED STATES (2477)
o UNITED STATES MINOR OUTLYING ISLANDS (2478)
o URUGUAY (2479)
o UZBEKISTAN (2480)
o VANUATU (2481)
                                                210
o VENEZUELA, BOLIVARIAN REPUBLIC OF (2482)
o VIETNAM (2483)
o VIRGIN ISLANDS, BRITISH (2484)
o VIRGIN ISLANDS, U.S. (2485)
o WALLIS AND FUTUNA (2486)
o WESTERN SAHARA (2487)
o YEMEN (2488)
o ZAMBIA (2489)
o ZIMBABWE (2490)
o Don't know/ Prefer not to say (2491)




                                             211
cps19_bornin_other Dans quel pays êtes-vous né?

   o AFGHANISTAN (2243)
   o ILES ALAND (2244)
   o ALBANIE (2245)
   o ALGÉRIE (2246)
   o SAMOA AMÉRICAINE (2247)
   o ANDORRA (2248)
   o ANGOLA (2249)
   o ANGUILLA (2250)
   o ANTARCTIQUE (2251)
   o ANTIGUA-ET-BARBUDA (2252)
   o ARGENTINE (2253)
   o ARMÉNIE (2254)
   o ARUBA (2255)
   o AUSTRALIE (2256)
   o AUTRICHE (2257)
   o AZERBAÏDJAN (2258)
   o BAHAMAS (2259)
   o BAHREIN (2260)
   o BANGLADESH (2261)

                                                  212
o BARBADE (2262)
o BÉLARUS (2263)
o BELGIQUE (2264)
o BELIZE (2265)
o BENIN (2266)
o BERMUDES (2267)
o BHOUTAN (2268)
o BOLIVIE, ÉTAT PLURINATIONAL DE (2269)
o BONAIRE, SAINT EUSTATIUS ET SABA (2270)
o BOSNIE HERZÉGOVINE (2271)
o BOTSWANA (2272)
o BOUVET ISLAND (2273)
o BRÉZIL (2274)
o TERRITOIRE BRITANNIQUE DE L'OCEAN INDIEN (2275)
o BRUNEI DARUSSALAM (2276)
o BULGARIE (2277)
o BURKINA FASO (2278)
o BURUNDI (2279)
o CAMBODGE (2280)
o CAMEROUN (2281)
                                                    213
o CAP-VERT (2282)
o ÎLES CAÏMANS (2283)
o RÉPUBLIQUE CENTRAFRICAINE (2284)
o TCHAD (2285)
o CHILI (2286)
o CHINE (2287)
o L'ÎLE DE NOËL (2288)
o ÎLES COCOS (KEELING) (2289)
o COLOMBIE (2290)
o COMORES (2291)
o CONGO (2292)
o CONGO, RÉPUBLIQUE DÉMOCRATIQUE DU (2293)
o LES ÎLES COOK (2294)
o COSTA RICA (2295)
o CÔTE D'IVOIRE (2296)
o CROATIE (2297)
o CUBA (2298)
o CURACAO (2299)
o CHYPRE (2300)
o RÉPUBLIQUE TCHÈQUE (2301)
                                             214
o DANEMARK (2302)
o DJIBOUTI (2303)
o DOMINICA (2304)
o RÉPUBLIQUE DOMINICAINE (2305)
o ÉQUATEUR (2306)
o ÉGYPTE (2307)
o LE SALVADOR (2308)
o GUINÉE ÉQUATORIALE (2309)
o ERYTHREE (2310)
o ESTONIE (2311)
o ETHIOPIE (2312)
o ÎLES FALKLAND (MALVINAS) (2313)
o ÎLES FÉROÉ (2314)
o FIJI (2315)
o FINLANDE (2316)
o FRANCE (2317)
o GUINÉE FRANÇAISE (2318)
o POLYNÉSIE FRANÇAISE (2319)
o TERRITOIRES DU SUD FRANÇAIS (2320)
o GABON (2321)
                                       215
o GAMBIE (2322)
o GEORGIE (2323)
o ALLEMAGNE (2324)
o GHANA (2325)
o GIBRALTAR (2326)
o GRÈCE (2327)
o GROENLAND (2328)
o GRENADE (2329)
o GUADELOUPE (2330)
o GUAM (2331)
o GUATEMALA (2332)
o GUERNSEY (2333)
o GUINÉE (2334)
o GUINEE-BISSAU (2335)
o GUYANE (2336)
o HAITI (2337)
o HEARD ISLAND ET LES ÎLES MCDONALD (2338)
o SAINT-SIÈGE (ÉTAT DE LA VILLE DU VATICAN) (2339)
o HONDURAS (2340)
o HONG KONG (2341)
                                                     216
o HUNGRIE (2342)
o ISLANDE (2343)
o INDE (2344)
o INDONESIE (2345)
o IRAN (RÉPUBLIQUE ISLAMIQUE D (2346)
o IRAK (2347)
o IRLANDE (2348)
o ISLE OF MAN (2349)
o ISRAËL (2350)
o ITALIE (2351)
o JAMAÏQUE (2352)
o JAPON (2353)
o JERSEY (2354)
o JORDAN (2355)
o KAZAKHSTAN (2356)
o KENYA (2357)
o KIRIBATI (2358)
o RÉPUBLIQUE POPULAIRE DÉMOCRATIQUE DE CORÉE (2359)
o CORÉE, RÉPUBLIQUE DE (2360)
o KOWEIT (2361)
                                                      217
o KYRGYZSTAN (2362)
o RÉPUBLIQUE DÉMOCRATIQUE POPULAIRE LAO (2363)
o LETTONIE (2364)
o LIBAN (2365)
o LESOTHO (2366)
o LIBÉRIA (2367)
o LIBYE (2368)
o LIECHTENSTEIN (2369)
o LITUANIE (2370)
o LUXEMBOURG (2371)
o MACAO (2372)
o MACÉDOINE, EX-RÉPUBLIQUE YOUGOSLAVE DE (2373)
o MADAGASCAR (2374)
o MALAWI (2375)
o MALAISIE (2376)
o MALDIVES (2377)
o MALI (2378)
o MALTE (2379)
o ILES MARSHALL (2380)
o MARTINIQUE (2381)
                                                  218
o MAURITANIE (2382)
o MAURICE (2383)
o MAYOTTE (2384)
o MEXIQUE (2385)
o MICRONESIE, ETATS FEDERES DE (2386)
o MOLDOVA, RÉPUBLIQUE DE (2387)
o MONACO (2388)
o MONGOLIE (2389)
o MONTÉNÉGRO (2390)
o MONTSERRAT (2391)
o MAROC (2392)
o MOZAMBIQUE (2393)
o MYANMAR (2394)
o NAMIBIE (2395)
o NAURU (2396)
o NÉPAL (2397)
o PAYS-BAS (2398)
o NOUVELLE CALÉDONIE (2399)
o NOUVELLE-ZÉLANDE (2400)
o NICARAGUA (2401)
                                        219
o NIGER (2402)
o NIGERIA (2403)
o NIUE (2404)
o L'ILE DE NORFOLK (2405)
o ÎLES MARIANNES DU NORD (2406)
o NORVÈGE (2407)
o OMAN (2408)
o PAKISTAN (2409)
o PALAU (2410)
o TERRITOIRE PALESTINIEN OCCUPÉ (2411)
o PANAMA (2412)
o PAPOUASIE NOUVELLE GUINÉE (2413)
o PARAGUAY (2414)
o PÉROU (2415)
o PHILIPPINES (2416)
o PITCAIRN (2417)
o POLOGNE (2418)
o PORTUGAL (2419)
o PUERTO RICO (2420)
o QATAR (2421)
                                         220
o RÉUNION (2422)
o ROUMANIE (2423)
o FÉDÉRATION RUSSE (2424)
o RWANDA (2425)
o SAINT BARTHÉLEMY (2426)
o Sainte-Hélène, ASCENSION ET TRISTAN DA CUNHA (2427)
o SAINT-CHRISTOPHE-ET-NIÉVÈS (2428)
o SAINTE-LUCIE (2429)
o SAINT MARTIN (PARTIE FRANCAISE) (2430)
o SAINT PIERRE ET MIQUELON (2431)
o SAINT-VINCENT-ET-LES-GRENADINES (2432)
o SAMOA (2433)
o SAINT MARIN (2434)
o SAO TOME ET PRINCIPE (2435)
o ARABIE SAOUDITE (2436)
o SÉNÉGAL (2437)
o SERBIE (2438)
o LES SEYCHELLES (2439)
o SIERRA LEONE (2440)
o SINGAPOUR (2441)
                                                        221
o SINT MAARTEN (PARTIE NEERLANDAISE) (2442)
o SLOVAQUIE (2443)
o SLOVÉNIE (2444)
o ÎLES SALOMON (2445)
o SOMALIE (2446)
o AFRIQUE DU SUD (2447)
o GÉORGIE DU SUD ET ÎLES SANDWICH DU SUD (2448)
o SOUDAN DU SUD (2449)
o ESPAGNE (2450)
o SRI LANKA (2451)
o SUDAN (2452)
o SURINAME (2453)
o SVALBARD ET JAN MAYEN (2454)
o SWAZILAND (2455)
o SUÈDE (2456)
o SUISSE (2457)
o RÉPUBLIQUE ARABE SYRIENNE (2458)
o TAIWAN, PROVINCE DE CHINE (2459)
o TAJIKISTAN (2460)
o TANZANIE, RÉPUBLIQUE UNIE DE (2461)
                                                  222
o THAÏLANDE (2462)
o TIMOR-LESTE (2463)
o TOGO (2464)
o TOKELAU (2465)
o TONGA (2466)
o TRINITÉ-ET-TOBAGO (2467)
o TUNISIE (2468)
o TURQUIE (2469)
o TURKMENISTAN (2470)
o ÎLES TURQUES-ET-CAÏQUES (2471)
o TUVALU (2472)
o UGANDA (2473)
o UKRAINE (2474)
o EMIRATS ARABES UNIS (2475)
o ROYAUME-UNI (2476)
o ÉTATS-UNIS (2477)
o ÎLES MINEURES ÉLOIGNÉES DES ÉTATS-UNIS (2478)
o URUGUAY (2479)
o UZBEKISTAN (2480)
o VANUATU (2481)
                                                  223
  o VENEZUELA, RÉPUBLIQUE BOLIVARIENNE DU (2482)
  o VIETNAM (2483)
  o ÎLES VIERGES, BRITANNIQUE (2484)
  o ILES VIERGES, ÉTATS-UNIS (2485)
  o WALLIS ET FUTUNA (2486)
  o SAHARA OCCIDENTAL (2487)
  o YÉMEN (2488)
  o ZAMBIE (2489)
  o ZIMBABWE (2490)
  o Je ne sais pas / Préfère ne pas répondre (2491)
Page Break




                                                      224
Display This Question:
    If Were you born in Canada? = No




                                       225
cps19_imm_year In what year did you come to live in Canada?

   o 1920 (306)
   o 1921 (307)
   o 1922 (308)
   o 1923 (309)
   o 1924 (310)
   o 1925 (311)
   o 1926 (312)
   o 1927 (313)
   o 1928 (314)
   o 1929 (315)
   o 1930 (316)
   o 1931 (317)
   o 1932 (318)
   o 1933 (319)
   o 1934 (320)
   o 1935 (321)
   o 1936 (322)
   o 1937 (323)
   o 1938 (324)

                                                              226
o 1939 (325)
o 1940 (326)
o 1941 (327)
o 1942 (328)
o 1943 (329)
o 1944 (330)
o 1945 (331)
o 1946 (332)
o 1947 (333)
o 1948 (334)
o 1949 (335)
o 1950 (336)
o 1951 (337)
o 1952 (338)
o 1953 (339)
o 1954 (340)
o 1955 (341)
o 1956 (342)
o 1957 (343)
o 1958 (344)
               227
o 1959 (345)
o 1960 (346)
o 1961 (347)
o 1962 (348)
o 1963 (349)
o 1964 (350)
o 1965 (351)
o 1966 (352)
o 1967 (353)
o 1968 (354)
o 1969 (355)
o 1970 (356)
o 1971 (357)
o 1972 (358)
o 1973 (359)
o 1974 (360)
o 1975 (361)
o 1976 (362)
o 1977 (363)
o 1978 (364)
               228
o 1979 (365)
o 1980 (366)
o 1981 (367)
o 1982 (368)
o 1983 (369)
o 1984 (370)
o 1985 (371)
o 1986 (372)
o 1987 (373)
o 1988 (374)
o 1989 (375)
o 1990 (376)
o 1991 (377)
o 1992 (378)
o 1993 (379)
o 1994 (380)
o 1995 (381)
o 1996 (382)
o 1997 (383)
o 1998 (384)
               229
o 1999 (385)
o 2000 (386)
o 2001 (387)
o 2002 (388)
o 2003 (389)
o 2004 (390)
o 2005 (391)
o 2006 (392)
o 2007 (393)
o 2008 (394)
o 2009 (395)
o 2010 (396)
o 2011 (397)
o 2012 (398)
o 2013 (399)
o 2014 (400)
o 2015 (401)
o 2016 (402)
o 2017 (403)
o 2018 (404)
               230
o 2019 (405)
o Don't know/ Prefer not to answer (406)




                                           231
cps19_imm_year En quelle année êtes-vous venu vivre au Canada?

   o 1920 (306)
   o 1921 (307)
   o 1922 (308)
   o 1923 (309)
   o 1924 (310)
   o 1925 (311)
   o 1926 (312)
   o 1927 (313)
   o 1928 (314)
   o 1929 (315)
   o 1930 (316)
   o 1931 (317)
   o 1932 (318)
   o 1933 (319)
   o 1934 (320)
   o 1935 (321)
   o 1936 (322)
   o 1937 (323)
   o 1938 (324)

                                                                 232
o 1939 (325)
o 1940 (326)
o 1941 (327)
o 1942 (328)
o 1943 (329)
o 1944 (330)
o 1945 (331)
o 1946 (332)
o 1947 (333)
o 1948 (334)
o 1949 (335)
o 1950 (336)
o 1951 (337)
o 1952 (338)
o 1953 (339)
o 1954 (340)
o 1955 (341)
o 1956 (342)
o 1957 (343)
o 1958 (344)
               233
o 1959 (345)
o 1960 (346)
o 1961 (347)
o 1962 (348)
o 1963 (349)
o 1964 (350)
o 1965 (351)
o 1966 (352)
o 1967 (353)
o 1968 (354)
o 1969 (355)
o 1970 (356)
o 1971 (357)
o 1972 (358)
o 1973 (359)
o 1974 (360)
o 1975 (361)
o 1976 (362)
o 1977 (363)
o 1978 (364)
               234
o 1979 (365)
o 1980 (366)
o 1981 (367)
o 1982 (368)
o 1983 (369)
o 1984 (370)
o 1985 (371)
o 1986 (372)
o 1987 (373)
o 1988 (374)
o 1989 (375)
o 1990 (376)
o 1991 (377)
o 1992 (378)
o 1993 (379)
o 1994 (380)
o 1995 (381)
o 1996 (382)
o 1997 (383)
o 1998 (384)
               235
o 1999 (385)
o 2000 (386)
o 2001 (387)
o 2002 (388)
o 2003 (389)
o 2004 (390)
o 2005 (391)
o 2006 (392)
o 2007 (393)
o 2008 (394)
o 2009 (395)
o 2010 (396)
o 2011 (397)
o 2012 (398)
o 2013 (399)
o 2014 (400)
o 2015 (401)
o 2016 (402)
o 2017 (403)
o 2018 (404)
               236
  o 2019 (405)
  o Je ne sais pas / Préfère ne pas répondre (406)
Page Break

NOTE: The introductory text to cps19_ethnicity varied based on whether
the respondent was a Canadian citizen or permanent resident. For
citizens, ${e://Field/ethnicity_intro} read “In addition to being
Canadian, to what ethnic or cultural group(s) do you belong?”, and for
permanent residents it read “To what ethnic or cultural group(s) do
you belong?”. In the French translation,
${e://Field/ethnicity_intro_fr} contained equivalent text.




                                                                    237
cps19_ethnicity ${e://Field/ethnicity_intro} Please select all that apply.

Please click the forward arrow → below once you are done.


   ▢           Aboriginal/ First Nations (23)


   ▢           British (24)


   ▢           Chinese (25)


   ▢           Dutch (26)


   ▢           English (27)


   ▢           French (28)


   ▢           French Canadian (29)


   ▢           German (30)


   ▢           Hispanic (31)


   ▢           Indian (32)


   ▢           Inuk/ Inuit (33)


   ▢           Irish (34)


   ▢           Italian (35)


   ▢           Métis (36)




                                                                             238
   ▢           Polish (37)


   ▢           Québécois (38)


   ▢           Scottish (39)


   ▢           Ukrainian (40)


   ▢        Other 1 (please specify) (41)
   ________________________________________________


   ▢        Other 2 (please specify) (42)
   ________________________________________________


   ▢           ⊗Don't know/ Prefer not to answer (43)
cps19_ethnicity ${e://Field/ethnicity_intro_fr} Veuillez sélectionner toutes les options qui
s'appliquent.




                                                                                               239
Veuillez cliquer sur la flèche → ci-dessous lorsque vous avez terminé.


   ▢          Autochtone/ Premières Nations (23)


   ▢          Britanique (24)


   ▢          Chinois (25)


   ▢          Néerlandais (26)


   ▢          Anglais (27)


   ▢          Français (28)


   ▢          Canadien français (29)


   ▢          Allemand (30)


   ▢          Hispanique (31)


   ▢          Indien (32)


   ▢          Inuk / Inuit (33)


   ▢          Irlandais (34)


   ▢          Italien (35)


   ▢          Métis (36)


   ▢          Polonais (37)


                                                                         240
  ▢          Québécois (38)


  ▢          Écossais (39)


  ▢          Ukrainien (40)


  ▢        Autre 1 (veuillez spécifier) (41)
  ________________________________________________


  ▢        Autre 2 (veuillez spécifier) (42)
  ________________________________________________


  ▢          ⊗Je ne sais pas / Préfère ne pas répondre (43)

Page Break




                                                              241
cps19_sexuality Do you consider yourself to be:

   o Heterosexual (1)
   o Homosexual (2)
   o Bisexual (3)
   o Other (4) ________________________________________________
   o Don't know (5)
   o Prefer not to say (6)
cps19_sexuality Vous considérez-vous comme étant :

   o Hétérosexuel (1)
   o Homosexuel (2)
   o Bisexuel (3)
   o Autre (4) ________________________________________________
   o Je ne sais pas (5)
   o Préfère ne pas répondre (6)
Page Break




                                                                  242
243
cps19_language Which language(s) did you learn as a child and still understand today? (Select
all that apply)


   ▢          English (68)


   ▢          French (69)


   ▢        Aboriginal language (please specify) (70)
   ________________________________________________


   ▢          Arabic (71)


   ▢          Chinese, Cantonese, Mandarin (72)


   ▢          Filipino / Tagalog (73)


   ▢          German (74)


   ▢          Indian, Hindi, Gujarati (75)


   ▢          Italian (76)


   ▢          Korean (77)


   ▢          Pakistani, Punjabi, Urdu (78)


   ▢          Persian, Farsi (79)


   ▢          Russian (80)


   ▢          Spanish (81)




                                                                                          244
▢       Tamil (82)


▢       Vietnamese (83)


▢        Other (please specify) (84)
________________________________________________


▢       ⊗Don't know/ Prefer not to answer (85)




                                                   245
cps19_language Quelle est la/les première(s) langue(s) que vous avez apprise(s) et que vous
comprenez encore? (Sélectionnez toutes celles qui s' appliquent)


   ▢          Anglais (68)


   ▢          Français (69)


   ▢        Langue autochtone (veuillez préciser) (70)
   ________________________________________________


   ▢          Arabe (71)


   ▢          Chinois, cantonais, mandarin (72)


   ▢          Philippin / tagalog (73)


   ▢          Allemand (74)


   ▢          Indien, Hindi, Gujarati (75)


   ▢          Italien (76)


   ▢          Coréen (77)


   ▢          Pakistanais, Pendjabi, Ourdou (78)


   ▢          Persan, farsi (79)


   ▢          Russe (80)


   ▢          Espagnol (81)




                                                                                         246
  ▢          Tamil (82)


  ▢          Vietnamien (83)


  ▢        Autre (Veuillez spécifier) (84)
  ________________________________________________


  ▢          ⊗Je ne sais pas / Préfère ne pas répondre (85)

Page Break




                                                              247
cps19_employment What is your employment status? Are you currently…

   o Working for pay full-time (1)
   o Working for pay part-time (2)
   o Self employed (with or without employees) (3)
   o Retired (4)
   o Unemployed/ looking for work (5)
   o Student (6)
   o Caring for a family (7)
   o Disabled (8)
   o Student and working for pay (9)
   o Caring for family and working for pay (10)
   o Retired and working for pay (11)
   o Other (please specify) (12) ________________________________________________
   o Don't know/ Prefer not to answer (13)




                                                                              248
cps19_employment Quel est votre statut d'emploi actuel?

   o Salarié à temps plein (1)
   o Salarié à temps partiel (2)
   o Travailleur autonome (avec ou sans employés) (3)
   o À la retraite (4)
   o Au chômage/à la recherche d'un travail (5)
   o Étudiant (6)
   o En charge d'une famille (7)
   o Handicapé (8)
   o Étudiant et salarié (9)
   o En charge d'une famille et salarié (10)
   o À la retraite et salarié (11)
   o Autre (veuillez spécifier) (12)
   ________________________________________________

   o Je ne sais pas / Préfère ne pas répondre (13)
Page Break




                                                          249
Display This Question:
    If What is your employment status? Are you currently… = Working for pay full-time
    Or What is your employment status? Are you currently… = Working for pay part-time


cps19_sector Do you work in the private sector, public sector, or non-profit sector?

   o Private sector (1)
   o Public sector (2)
   o Non-profit sector (4)
   o Don't know/ Prefer not to answer (5)
cps19_sector Travaillez-vous dans le secteur privé, le secteur public, ou le secteur à but non
lucratif?

   o Secteur privé (1)
   o Secteur public (2)
   o Secteur à but non lucratif (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
Page Break




                                                                                             250
cps19_union Do you belong to a union?

   o Yes (1)
   o No (2)
   o Don’t know/ Prefer not to say (3)
cps19_union Appartenez-vous à un syndicat?

   o Oui (1)
   o Non (2)
   o Je ne sais pas / Préfère ne pas répondre (3)
Page Break




                                                    251
cps19_children Do you have any children?

   o Yes (1)
   o No (2)
   o Don't know/ Prefer not to answer (3)
cps19_children Avez-vous des enfants?

   o Oui (1)
   o Non (2)
   o Je ne sais pas / Préfère ne pas répondre (3)
Page Break




                                                    252
cps19_income_number What was your total household income, before taxes, for the year
2018? Be sure to include income from all sources, to the nearest thousand dollars.

For example, if your household had a total before-tax income of $71,336 in 2018, you would
enter 71000.

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

cps19_income_number Quel est le revenu total de votre ménage avant impôts en 2018? Cela
doit inclure toutes les sources de revenus au millier de dollars près.

Par exemple, si votre revenus total avant impôts était de 71 336$ en 2018, entrez 71000.

Si vous ne savez pas, ou préférez ne pas répondre, veuillez cliquer sur la flèche →

    ________________________________________________________________



Page Break




                                                                                             253
Display This Question:
    If If What was your total household income, before taxes, for the year 2018? Be sure to include
income from all sources, to the nearest thousand dollars.For example, if your household had a total
before-... Text Response Is Empty
    And What was your total household income, before taxes, for the year 2018? Be sure to include
income from all sources, to the nearest thousand dollars.For example, if your household had a total
before-... Text Response Is Not Equal to 0


cps19_income_cat We don't need the exact amount; does your household income fall into one
of these broad categories?

    o No income (1)
    o $1 to $30,000 (2)
    o $30,001 to $60,000 (3)
    o $60,001 to $90,000 (4)
    o $90,001 to $110,000 (5)
    o $110,001 to $150,000 (6)
    o $150,001 to $200,000 (7)
    o More than $200,000 (8)
    o Don't know/ Prefer not to answer (9)




                                                                                                      254
cps19_income_cat Nous n'avons pas besoin du montant exact; le revenu de votre ménage se
situe-t-il dans l'une des catégories suivantes?

   o Aucun revenu (1)
   o 1$ à 30 000$ (2)
   o 30 001$ à 60 000$ (3)
   o 60 001$ à 90 000$ (4)
   o 90 001$ à 110 000$ (5)
   o 110 001$ à 150 000$ (6)
   o 150 001$ à 200 000$ (7)
   o Plus de 200 000$ (8)
   o Je ne sais pas / Préfère ne pas répondre (9)
Page Break




                                                                                     255
cps19_property Do you or a member of your household own a residence (for example, a home
or an apartment), own a business (for example, a piece of property, a farm, or livestock), have
stocks or bonds, or have savings? Please check all that apply.

Please click the forward arrow → below once you are done.


   ▢          Own a residence (1)


   ▢          Own a business, a piece of property, a farm or livestock (2)


   ▢          Own stocks or bonds (3)


   ▢          Have any savings (4)


   ▢          ⊗None of these (5)

   ▢          ⊗Don't know/ Prefer not to answer (6)
cps19_property
Est-ce que vous ou un membre de votre ménage possédez une résidence (par exemple, une
maison ou un appartement), une entreprise (par exemple, une propriété, une ferme ou un
élevage), avez des actions ou des obligations, ou des économies? Veuillez sélectionner toutes




                                                                                            256
les options qui s'appliquent.
 Veuillez cliquer sur la flèche → ci-dessous lorsque vous avez terminé.


   ▢          Possède une résidence (1)


   ▢          Possède une entreprise, une propriété, une ferme ou un élevage (2)


   ▢          Possède des actions ou des obligations (3)


   ▢          Possède des économies (4)


   ▢          ⊗Aucun (5)

   ▢          ⊗Je ne sais pas / Préfère ne pas répondre (6)

Page Break




                                                                                   257
cps19_marital Are you presently married, living with a partner, divorced, separated, widowed, or
have you never been married?

   o Married (1)
   o Living with a partner (2)
   o Divorced (3)
   o Separated (4)
   o Widowed (5)
   o Never Married (6)
   o Don't know/ Prefer not to answer (7)
cps19_marital Êtes-vous présentement marié(e), vivant avec un(e) conjoint(e), divorcé(e),
séparé(e), veuf (veuve), ou n'avez-vous jamais été marié(e)?

   o Marié(e) (1)
   o Vivant(e) avec un conjoint(e) de fait (2)
   o Divorcé(e) (3)
   o Séparé(e) (4)
   o Veuf/veuve (5)
   o Jamais marié(e) (6)
   o Je ne sais pas / Préfère ne pas répondre (7)
Page Break



                                                                                            258
259
cps19_household Counting yourself how many people live in your household?

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

cps19_household En vous incluant, combien de personnes votre ménage comporte-t-il?

Si vous ne savez pas, ou préférez ne pas répondre, veuillez sélectionner →

    ________________________________________________________________


End of Block: Additional demographics




                                                                                     260
   9. Post Election Survey

   9.1 Metadata

pes19_StartDate
Start timestamp for the Post Election Survey response, in Stata time format

pes19_EndDate
End timestamp for the Campaign Period Survey response, in Stata time format

pes19_ResponseId
Unique identification code of the Post Election Survey response. Mainly useful for data
management, such as combining different versions of the dataset.

pes19_current_date
Date the Post Election Survey response started, in YYYYMMDD format, as a number.
For example, “20191020” would be October 20, 2019.

pes19_current_date_string
Date the Post Election Survey response started, in YYYYMMDD format, as a string.
For example, “20191020” would be October 20, 2019.

pes19_Q_Language
Language the respondent answered the Post Election Survey in. “EN” is English, “FR-CA” is
French.

pes19_Q_TotalDuration
How long the respondent spent in the Post Election Survey, in seconds. This includes all time
from when the survey is opened, to when the response is submitted, including time spent away
from the survey, and if the respondent closes the survey and returns to it later.

pes19_fsa
The first three digits of the respondent’s postal code from the Post Election Survey, also known
as their Forward Sortation Area. This is provided instead of respondents’ full postal code to
protect their privacy.

notvote_split
An embedded data field used to record the assigned treatment for a question type experiment.
notvote_split was randomly set to either “categorical” or “textbox”. If notvote_split was
“categorical” (and the respondent did not vote), the respondent received the question
pes19_notvotereason1, which was a categorical question listing potential reasons why they did
not vote, and asking them to select the main reason. If notvote_split was “textbox” (and the



                                                                                             261
respondent did not vote), the respondent received the question pes19_notvotereason2, which
provided a text box for the respondent to write in the main reason why they did not vote.

splitsample
This embedded data determined which of two large sets of questions the respondent would
receive, either “CSES” for a set of questions related to the Comparative Study of Electoral
Systems (CSES), or “modules”, for a second set of attitudinal questions largely focused on
respondents' experience with the electoral process. The two sets of questions were designed to
take roughly the same amount of time for respondents to complete. The lists below show which
questions the respondent received if they were in each category, assuming they met all other
criteria for those questions.

   •   CSES
         o pes19_can_id
         o pes19_ottawa_perf
         o pes19_party_rep
         o pes19_party_rep_whic
         o pes19_party_rate
         o pes19_lead_rate
         o pes19_lr_parties
         o pes19_lr_self
   •   modules
         o pes19_likert_int_emb
         o pes19_emb_none
         o pes19_emb_id
         o pes19_emb_vote16
         o pes19_lowturnout
         o pes19_internetvote1
         o pes19_internetvote2
         o pes19_conf_inst1
         o pes19_conf_inst2
         o pes19_foreign
         o pes19_emb_satif
         o pes19_emb8
         o pes19_internetregis
         o pes19_internetrisk1
         o pes19_internetrisk2
         o pes19_emb_register
         o pes19_emb_card
         o pes19_emb_register2
         o pes19_emb_reg_how
         o pes19_emb_register3
         o pes19_emb4



                                                                                           262
           o   pes19_emb7
           o   pes19_emb_info
           o   pes19_provvote

confidence_institutions_word
confidence_institutions_word_fr
These embedded data fields were used in a wording experiment, in which
confidence_institutions_word (which was piped into
${e://Field/confidence_institutions_word} ) was randomly set to be either
“confident” in English (“confiant” in French) or “worried” (“inquiet” in French) for the question
pes19_foreign.

govt_programs_word
govt_programs_word_fr
These embedded data fields were used in a wording experiment, in which govt_programs_word
(which was piped into ${e://Field/ govt_programs_word} ) was randomly set to be
either “afford” in English (“n’a plus les moyens” in French) or “deliver” (“ne peut plus offrir” in
French) for the question pes19_govtprograms.

split_taxes
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question pes19_taxes. 1 = respondent received pes19_taxes, 0 = they did not.

split_senate
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question pes19_senate. 1 = respondent received pes19_senate, 0 = they did
not.

split_trade
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question pes19_trade. 1 = respondent received pes19_trade, 0 = they did not.

split_lifesat
Randomized embedded data field containing a flag indicating whether the respondent would
receive the questions pes19_happy and pes19_satisfied. 1 = respondent received
pes19_happy and pes19_satisfied, 0 = they did not.

split_responsibility
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question pes19_cognition. 1 = respondent received pes19_cognition, 0 =
they did not.

split_sexism


                                                                                                    263
Randomized embedded data field containing a flag indicating whether the respondent would
receive the questions on sexism: pes19_hostile1, pes19_hostile2,
pes19_hostile3, pes19_benevolent1, pes19_benevolent2, and
pes19_benevolent3. 1 = respondent received the questions on sexism, 0 = they did not.

split_abortion
Randomized embedded data field containing a flag indicating whether the respondent would
receive ONE of the questions on abortion: pes19_abort1, pes19_abort2,
pes19_abort3, pes19_abort4, pes19_abort5, or pes19_abort6. 1 = respondent
received one of the questions on abortion, 0 = they did not.

split_getahead
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question pes19_blame and pes19_stdofliving. 1 = respondent received
pes19_blame and pes19_stdofliving, 0 = they did not.

split_att_div
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question pes19_fitin and pes19_immigjobs. 1 = respondent received
pes19_fitin and pes19_immigjobs, 0 = they did not.

split_govt_eff
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question pes19_govteff and pes19_govtprograms. 1 = respondent received
QNAME, 0 = they did not.

split_medical
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question pes19_paymed. 1 = respondent received pes19_paymed, 0 = they did
not.

split_ties
Randomized embedded data field containing a flag indicating whether the respondent would
receive the questions pes19_tieus, pes19_tiechina, and pes19_country. 1 =
respondent received pes19_tieus, pes19_tiechina, and pes19_country, 0 = they
did not.

split_health_followups
Randomized embedded data field containing a flag indicating whether the respondent would
receive the follow-up health questions pes19_phealth and pes19_mhealth. 1 =
respondent received pes19_phealth and pes19_mhealth, 0 = they did not.




                                                                                           264
split_gender_id
Randomized embedded data field containing a flag indicating whether the respondent would
receive the questions pes19_feminine and pes19_masculine. 1 = respondent received
pes19_feminine and pes19_masculine, 0 = they did not.

split_big5
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question pes19_big5. 1 = respondent received pes19_big5, 0 = they did not.

split_hatespeech
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question pes19_hatespeech. 1 = respondent received pes19_hatespeech, 0 =
they did not.

split_vol_assoc
Randomized embedded data field containing a flag indicating whether the respondent would
receive the question pes19_volassoc. 1 = respondent received pes19_volassoc, 0 = they
did not.

PES19_data_quality

This embedded data field contains the most important data quality category that the respondent
is in, and was used during data review and cleaning. See section 6.2.2 for more details.

pes19_panel
Which panel the respondent was drawn from, measured during the Post Election Survey.

pes19_age
Respondent age in years recoded based on their year of birth, pes19_yob.

pes19_duplicates_flag
Indicator for respondents that took the Post Election Survey multiple times. 0 = Unique, 1 =
Initial response of someone who took the survey again. Any subsequent responses have
already been removed from the data.

pes19_inattentive
Indicator that respondent took more than 60 minutes to complete the Post Election Survey. 1 =
Inattentive.

pes19_weight_general_all
Sample weight for all Post Election Survey respondents. See section 5.3 for more details.




                                                                                               265
pes19_weight_general_restricted
Sample weight for Post Election Survey respondents, excluding subsequent duplicates and
inattentive respondents. See section 5.3 for more details.




                                                                                          266
   9.2 Survey flow
EmbeddedData
  current_date = ${date://CurrentDate/Y}${date://CurrentDate/m}${date://CurrentDate/d}
  Q_LanguageValue will be set from Panel or URL.
  Q_TotalDurationValue will be set from Panel or URL.
EmbeddedData
  testingValue will be set from Panel or URL.
  UserAgentValue will be set from Panel or URL.
  ip_address = ${loc://IPAddress}

BlockRandomizer: 1 -

   EmbeddedData
     notvote_split = categorical
   EmbeddedData
     notvote_split = textbox

BlockRandomizer: 1 -

   EmbeddedData
     splitsample = CSES
   EmbeddedData
     splitsample = modules

BlockRandomizer: 1 -

   EmbeddedData
     confidence_institutions_word = confident
   EmbeddedData
     confidence_institutions_word = worried

Branch: New Branch
   If
       If confidence_institutions_word Is Equal to confident

   EmbeddedData
     confidence_institutions_word_fr = confiant

Branch: New Branch
   If
       If confidence_institutions_word Is Equal to worried

   EmbeddedData
     confidence_institutions_word_fr = inquiet

BlockRandomizer: 1 -

   EmbeddedData


                                                                                   267
     govt_programs_word = afford
   EmbeddedData
     govt_programs_word = deliver

Branch: New Branch
   If
       If govt_programs_word Is Equal to afford

   EmbeddedData
     govt_programs_word_fr = n’a plus les moyens

Branch: New Branch
   If
       If govt_programs_word Is Equal to deliver

   EmbeddedData
     govt_programs_word_fr = ne peut plus offrir

BlockRandomizer: 1 -

   EmbeddedData
     split_taxes = 0
   EmbeddedData
     split_taxes = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_senate = 0
   EmbeddedData
     split_senate = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_trade = 0
   EmbeddedData
     split_trade = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_trade = 0
   EmbeddedData
     split_trade = 1

BlockRandomizer: 1 -

   EmbeddedData


                                                   268
     split_lifesat = 0
   EmbeddedData
     split_lifesat = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_responsibility = 0
   EmbeddedData
     split_responsibility = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_sexism = 0
   EmbeddedData
     split_sexism = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_abortion = 0
   EmbeddedData
     split_abortion = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_getahead = 0
   EmbeddedData
     split_getahead = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_att_div = 0
   EmbeddedData
     split_att_div = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_govt_eff = 0
   EmbeddedData
     split_govt_eff = 1

BlockRandomizer: 1 -

   EmbeddedData


                                269
     split_medical = 0
   EmbeddedData
     split_medical = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_ties = 0
   EmbeddedData
     split_ties = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_health_followups = 0
   EmbeddedData
     split_health_followups = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_gender_id = 0
   EmbeddedData
     split_gender_id = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_big5 = 0
   EmbeddedData
     split_big5 = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_hatespeech = 0
   EmbeddedData
     split_hatespeech = 1

BlockRandomizer: 1 -

   EmbeddedData
     split_vol_assoc = 0
   EmbeddedData
     split_vol_assoc = 1

Standard: Consent and basic demographics (4 Questions)

Branch: New Branch


                                                         270
    If
       If Letter of Information and Consent Project Title: Canadian Election Study
2019Principal Investigat... I consent to participate in this study. I have read all of the
information about the study. Is Not Selected

    EmbeddedData
      term = noconsent
      gc = 2

    EndSurvey: Advanced

Branch: New Branch
   If
       If Are you a... Other Is Selected

    EmbeddedData
      term = noncitizen_or_pr
      gc = 2

    EndSurvey: Advanced

Standard: Main issue (1 Question)
Standard: Voting part 1 - turnout (2 Questions)
Standard: Voting part 2 - Reason for voting or not voting (4 Questions)
Standard: Voting part 2 -vote choice (2 Questions)
Standard: Satisfaction with democracy (1 Question)
Standard: Attention to campaign (1 Question)
Standard: Parties contacted (2 Questions)
Standard: Legitimate mandate (1 Question)
Standard: Government formation (1 Question)
Standard: Parties keep promises (1 Question)
Standard: Groups thermometers (2 Questions)

Branch: New Branch
   If
       If In which province or territory are you currently living? Quebec Is Selected

    BlockRandomizer: 1 -

         Standard: Few words on each party - Liberal Party (1 Question)
         Standard: Few words on each party - Conservative Party (1 Question)
         Standard: Few words on each party - New Democratic Party (1 Question)
         Standard: Few words on each party - Bloc Quebecois (1 Question)
         Standard: Few words on each party - Green Party (1 Question)
         Standard: Few words on each party - People's Party (1 Question)

Branch: New Branch



                                                                                             271
   If
        If In which province or territory are you currently living? Quebec Is Not Selected

   BlockRandomizer: 1 -

        Standard: Few words on each party - Liberal Party (1 Question)
        Standard: Few words on each party - Conservative Party (1 Question)
        Standard: Few words on each party - New Democratic Party (1 Question)
        Standard: Few words on each party - Green Party (1 Question)
        Standard: Few words on each party - People's Party (1 Question)

Standard: Retrospective state of the economy (1 Question)
Standard: Likert section 1 intro (1 Question)
Standard: Statement: electoral reform (1 Question)

Branch: New Branch
   If
       If split_medical Is Equal to 1

   Standard: Position statements: Paid medical treatment (1 Question)

Branch: New Branch
   If
       If split_senate Is Equal to 1

   Standard: Other: statements: Senate (1 Question)

Standard: Issue positions - environment versus jobs (2 Questions)

BlockRandomizer: 3 -

   Branch: New Branch
      If
          If split_hatespeech Is Equal to 1

        Standard: Democracy Checkup - democratic values: hate speech (1 Question)

   Standard: Democracy Checkup - democratic values: lose touch (1 Question)
   Standard: Democracy Checkup - democratic values: women home (1 Question)

BlockRandomizer: 3 -

   Standard: Democracy Checkup - efficacy and government: govt care (1 Question)
   Standard: Efficacy - understand (2 Questions)
   Standard: Democracy Checkup - efficacy and government: family values (1 Question)

BlockRandomizer: 1 -

   BlockRandomizer: 1 -



                                                                                        272
       Standard: Democracy Checkup - democratic values: politicians lie (1 Question)

   BlockRandomizer: 2 -

       Standard: Democracy Checkup - attitudes towards diversity: bilingualism (1
       Question)
       Standard: Democracy Checkup - democratic values: equal rights (1 Question)

Standard: Democracy Checkup - attitudes towards diversity: group identity (1 Question)

Branch: New Branch
   If
       If split_att_div Is Equal to 1

   BlockRandomizer: 2 -

       Standard: Democracy Checkup - attitudes towards diversity: assimilation (1
       Question)
       Standard: Democracy Checkup - attitudes towards diversity: take jobs (1
       Question)

Branch: New Branch
   If
       If split_govt_eff Is Equal to 1

   BlockRandomizer: 2 -

       Standard: Democracy Checkup - efficacy and government: govt effectiveness (1
       Question)
       Standard: Democracy Checkup - efficacy and government: govt programs (1
       Question)

Branch: New Branch
   If
       If split_ties Is Equal to 1

   BlockRandomizer: 2 -

       Standard: Democracy Checkup: ties with US (1 Question)
       Standard: Democracy Checkup: ties with China (1 Question)

   Standard: Country Thermometers (2 Questions)

Branch: New Branch
   If
       If splitsample Is Equal to CSES

   Standard: CSES Canadian Identity (1 Question)
   Standard: CSES questions part 1 (3 Questions)


                                                                                    273
   Standard: CSES parties and leaders - Phone-to-web wording - Parties (1 Question)
   Standard: CSES parties and leaders - Phone-to-web wording - Leaders (1 Question)
   Standard: CSES Left - right scales (2 Questions)

Branch: New Branch
   If
       If splitsample Is Equal to modules

   Standard: EMB - statements (7 Questions)
   Standard: EMB - Democratic Checkup: confidence and federal satisfaction (5
   Questions)
   Standard: EMB - Internet voting (3 Questions)
   Standard: Elections Ontario 1 (6 Questions)
   Standard: Elections Ontario 2 (2 Questions)
   Standard: Other: Provincial election (1 Question)

Standard: Interest in politics (1 Question)
Standard: Democracy Checkup: social network (3 Questions)
Standard: Discussion of politics with Social Networks (3 Questions)

BlockRandomizer: 3 -

   Standard: Democracy Checkup: participation - protest (1 Question)
   Standard: Democracy Checkup: participation - institution (1 Question)
   Standard: Democracy Checkup: participation - civic (1 Question)

Branch: New Branch
   If
       If split_vol_assoc Is Equal to 1

   Standard: Participation battery: Voluntary associations (1 Question)

Standard: Party Member - Lifetime (1 Question)
Standard: Importance of voting (2 Questions)
Standard: Likert section 2 intro (1 Question)

BlockRandomizer: 3 -

   Standard: Media 1 (1 Question)
   Standard: Media 2 (1 Question)
   Standard: Media 3 (1 Question)

Standard: Media 4 (1 Question)
Standard: Statement: Protect women (1 Question)
Standard: Corruption (1 Question)
Standard: Populism battery intro (1 Question)

BlockRandomizer: 8 -



                                                                                 274
   Standard: Populism battery 1 (1 Question)
   Standard: Populism battery 2 (1 Question)
   Standard: Populism battery 3 (1 Question)
   Standard: Populism battery 4 (1 Question)
   Standard: Populism battery 5 (1 Question)
   Standard: Populism battery 6 (1 Question)
   Standard: Populism battery 7 (1 Question)
   Standard: Populism battery 8 (1 Question)

BlockRandomizer: 5 -

   Standard: Nativism battery 1 (1 Question)
   Standard: Nativism battery 2 (1 Question)
   Standard: Nativism battery 3 (1 Question)
   Standard: Nativism battery 4 (1 Question)
   Standard: Nativism battery 5 (1 Question)

Standard: Canadian identification (3 Questions)
Standard: SDO - intro (1 Question)

BlockRandomizer: 4 -

   Standard: SDO - 1 (1 Question)
   Standard: SDO - 2 (1 Question)
   Standard: SDO - 3 (1 Question)
   Standard: SDO - 4 (1 Question)

BlockRandomizer: 4 -

   Standard: How much should be done for... racial minorities (1 Question)
   Standard: How much should be done for... women (1 Question)
   Standard: How much should be done for... gays and lesbians (1 Question)
   Standard: How much should be done for... quebec (1 Question)

Branch: New Branch
   If
       If split_taxes Is Equal to 1

   Standard: Other: taxes (1 Question)

Branch: New Branch
   If
       If split_abortion Is Equal to 1

   Standard: Other: Abortion 1 (6 Questions)

Standard: Likert section 3 intro (1 Question)




                                                                             275
Branch: New Branch
   If
       If split_trade Is Equal to 1

   Standard: Statement: International Trade (1 Question)

Standard: Statement: Private sector and jobs (1 Question)
Standard: Statements: Government should act to reduce inequality (1 Question)
Standard: Statements: Deservingness (2 Questions)

Branch: New Branch
   If
       If split_getahead Is Equal to 1

   Standard: Get ahead & Govt should (2 Questions)

Standard: Trust (1 Question)
Standard: Inequality (1 Question)
Standard: Inequality gap (1 Question)
Standard: Strong fed or prov govt (1 Question)
Standard: Likert section 4 intro (1 Question)

Branch: New Branch
   If
       If split_sexism Is Equal to 1

   BlockRandomizer: 6 -

       Standard: Other: statements: Sexism - 1 (1 Question)
       Standard: Other: statements: Sexism - 2 (1 Question)
       Standard: Other: statements: Sexism - 3 (1 Question)
       Standard: Other: statements: Sexism - 4 (1 Question)
       Standard: Other: statements: Sexism - 5 (1 Question)
       Standard: Other: statements: Sexism - 6 (1 Question)

Standard: Climate change (2 Questions)

Branch: New Branch
   If
       If splitsample Is Equal to CSES

   Standard: CSES Party identification (4 Questions)

Branch: New Branch
   If
       If splitsample Is Equal to modules

   Standard: Party ID and membership part 1 (2 Questions)



                                                                                276
Branch: New Branch
   If
       If In federal politics, do you usually think of yourself as a: Liberal Is Selected
       Or Which party do you feel closest to? Liberal Party Is Selected

    EmbeddedData
      pid_en = Liberal
      pid_party_en = Liberal Party
      pid_party_fr = Parti libéral

Branch: New Branch
    If
       If In federal politics, do you usually think of yourself as a: Conservative Is
Selected
       Or Which party do you feel closest to? Conservative Party Is Selected

    EmbeddedData
      pid_en = Conservative
      pid_party_en = Conservative Party
      pid_party_fr = Parti conservateur

Branch: New Branch
   If
       If In federal politics, do you usually think of yourself as a: NDP Is Selected
       Or Which party do you feel closest to? NDP Is Selected

    EmbeddedData
      pid_en = NDP
      pid_party_en = NDP
      pid_party_fr = NPD

Branch: New Branch
    If
       If In federal politics, do you usually think of yourself as a: Bloc Québécois Is
Selected
       Or Which party do you feel closest to? Bloc Québécois Is Selected

    EmbeddedData
      pid_en = Bloc Québécois
      pid_party_en = Bloc Québécois
      pid_party_fr = Bloc québécois

Branch: New Branch
   If
       If In federal politics, do you usually think of yourself as a: Green Is Selected
       Or Which party do you feel closest to? Green Party Is Selected



                                                                                            277
    EmbeddedData
      pid_en = Green
      pid_party_en = Green Party
      pid_party_fr = Parti vert

Branch: New Branch
    If
       If In federal politics, do you usually think of yourself as a: People’s Party Is
Selected
       Or Which party do you feel closest to? People's Party Is Selected

    EmbeddedData
      pid_en = People's Party
      pid_party_en = People's Party
      pid_party_fr = Parti populaire

Branch: New Branch
   If
       If splitsample Is Equal to modules

    Standard: Party ID and membership part 2 (1 Question)

Standard: Affective PID (1 Question)

Branch: New Branch
   If
       If In which province or territory are you currently living? Quebec Is Selected

    Standard: Quebec: French Language & culture threat (2 Questions)
    Standard: Quebec seperation (2 Questions)

Standard: Likert section 5 intro (1 Question)
Standard: Statements: Newer lifestyles (1 Question)

Branch: New Branch
   If
       If split_lifesat Is Equal to 1

    Standard: Other: statements: Life Satisfaction (2 Questions)

Branch: New Branch
   If
       If split_responsibility Is Equal to 1

    Standard: Other: statements: responsibility (1 Question)

Branch: New Branch
   If



                                                                                          278
        If split_gender_id Is Equal to 1

    BlockRandomizer: 2 -

        Standard: Gender ID - feminine (1 Question)
        Standard: Gender ID - masculine (1 Question)

Branch: New Branch
   If
       If split_big5 Is Equal to 1

    Standard: Big 5 Word descriptions (1 Question)

Standard: Health - initial (1 Question)

Branch: New Branch
   If
       If split_health_followups Is Equal to 1

    BlockRandomizer: 2 -

        Standard: Health - follow-up physical (1 Question)
        Standard: Health - follow-up mental (1 Question)

Standard: Additional demographics (11 Questions)

EmbeddedData
  gc = 1

EndSurvey: Advanced
Page Break




                                                             279
   9.3 Questions

   9.3.1       Consent and basic demographics

Start of Block: Consent and basic demographics


pes19_consent
 Letter of Information and Consent
 Project Title: Canadian Election Study 2019
 Principal Investigator: Laura Stephenson, PhD, Political Science, University of Western
Ontario, (519) 661-2111x85164, laura.stephenson@uwo.ca
 Co-Investigators: Allison Harell, PhD, Political Science, Université de Québec à Montréal,
(514) 987-3000 x5676, harell.allison@uqam.ca
 Peter Loewen, PhD, Political Science, Munk School of Global Affairs, University of Toronto,
(416) 978-5120, peter.loewen@utoronto.ca
 Daniel Rubenson, PhD, Politics and Public Administration, Ryerson University, (416) 979-5000
x 4052, rubenson@ryerson.ca

 Thank you for considering taking our survey. You can complete the survey in English or in
French. Please choose your preferred language using the drop-down menu at the top right of
this screen (vous pouvez choisir de compléter ce sondage en français ou en anglais en
sélectionnant la langue de votre choix à l’aide du menu déroulant situé dans le coin supérieur
droit de l'écran).

 Today we are doing another part of a research project on Canadians' attitudes about current
events, elections and democracy, and we would like your opinions. You are being invited to
participate because you completed a survey for our project previously. Participation in this part
of the research is completely voluntary. Today’s survey will take about 20 minutes to
complete. Your answers will be kept completely confidential and will be used for research
purposes only.

 To read additional information and details about this study, including your rights as a research
participant, how you will be compensated for your time and how your data will be stored, please
click HERE. If you would like to complete the survey, please click the appropriate link below.

If you have questions at any time about the study or its results, you may contact:
Dr. Laura Stephenson
Department of Political Science
University of Western Ontario
London, Ontario, Canada
1-519-661-2111 ext. 85164
Laura.stephenson@uwo.ca




                                                                                              280
 If you have any questions about your rights as a research participant or the conduct of this
study, you may contact The Office of Human Research Ethics (519) 661-3036, 1-844-720-9816,
email: ethics@uwo.ca. This office oversees the ethical conduct of research studies and is not
part of the study team. Everything that you discuss will be kept confidential.

   o I consent to participate in this study. I have read all of the information about the study.
   (1)

   o I do not consent to participate. (2)
pes19_consent

 Lettre d'information et de consentement
 Titre du projet: Étude électorale canadienne 2019
 Chercheure principale: Laura Stephenson, PhD, Science politique, University of Western
Ontario, (519) 661 2111x85164, laura.stephenson@uwo.ca
 Cochercheurs: Allison Harell, PhD, Science politique, Université de Québec à Montréal, (514)
987-3000 x5676, harell.allison@uqam.ca
 Peter Loewen, PhD, Science politique , Munk School of Global Affairs, University of Toronto,
(416) 978-5120, peter.loewen@utoronto.ca
 Daniel Rubenson, PhD, Politique et administration publique, Ryerson University, (416) 979-
5000 x 4052, rubenson@ryerson.ca
 Merci de bien vouloir participer à notre sondage. Vous pouvez compléter ce sondage en
français ou en anglais. Veuillez sélectionner la langue de votre choix à l'aide du menu déroulant
dans le coin supérieur droit de l'écran. (You can complete the survey in English or in
French. Please choose your preferred language using the drop-down menu at the top right of
this screen).
 Nous effectuons une autre partie de l'étude portant sur les attitudes des Canadiens au sujet de
l'actualité, des élections et de la démocratie, et nous aimerions connaître votre opinion. Vous
êtes invité à participer parce que vous avez déjà participé à un autre sondage dans le cadre de
ce projet. Votre participation à cette partie de la recherche est totalement volontaire. Le
sondage d’aujourd’hui prendra environ 20 minutes. Vos réponses resteront totalement
confidentielles et seront utilisées à des fins de recherche uniquement.
 Pour obtenir des informations supplémentaires sur cette étude, incluant de l’information sur vos
droits en tant que participant, sur la compensation offerte en échange de votre temps ainsi que
sur la manière dont les données seront conservées, veuillez cliquer ICI. Pour compléter le
sondage, veuillez cliquer sur le lien ci-dessous.

 Pour toutes questions portant sur l'étude ou ses résultats, vous pouvez contacter en tout
temps:     Dre Laura Stephenson
 Département de science politique
 University of Western Ontario
 London, Ontario, Canada



                                                                                               281
1-519-661-2111 ext. 85164
Laura.stephenson@uwo.ca

 Pour toutes questions sur vos droits en tant que participant ou sur le déroulement de cette
étude, vous pouvez contacter le Bureau de l'éthique de la recherche humaine au (519) 661-
3036, 1-844-720-9816, ou par courriel: ethics@uwo.ca. Ce bureau s'assure du respect de
l'éthique et ne fait pas partie de l'équipe de recherche. Tout ce dont vous discuterez demeurera
confidentiel.

    o Je consens à participer à cette étude. J'ai lu toutes les informations à propos de l'étude.
    (1)

    o Je ne consens pas à participer. (2)
Skip To: End of Block If Letter of Information and Consent Project Title: Canadian Election Study
2019Principal Investigat... = I do not consent to participate.


NOTE: The “HERE” text (or “ICI” in the French side) in the consent
page led to another page, which would open in a new browser window or
tab, that contained the text below.7

NOTE: Respondents who did not consent to the survey were screened out.




additional_consent
Letter of Information and Consent – Additional Information


7
 This separate page was implemented as a separate survey in the Qualtrics platform, so that it could open in a new
window, and not have the respondent lose their place in the current survey session. Here’s how to set it up:

1. Create a separate survey for the additional information page, format and publish it

2. Add a hyperlink to the main consent page, that goes to the live survey link for the additional page. Make sure to set
the link to open in a new window (it's under the "edit link" options when you right-click on the link), so that they don't
lose their spot in the survey.

3. If you want to have the link go to the same language as the source page, you have to add "?Q_Language=EN" or
"?Q_Language=FR" (or whatever Qualtrics language codes are relevant).

JavaScript was added to remove the "next" button on the additional info page, so that they could only view the page,
not "complete" that survey and get to a completion page that might confuse them.


                                                                                                                     282
 Project Title: Canadian Election Study 2019
 Principal Investigator: Laura Stephenson, PhD, Political Science, University of Western
Ontario, (519) 661-2111x85164, laura.stephenson@uwo.ca
 Co-Investigators: Allison Harell, PhD, Political Science, Université de Québec à Montréal,
(514) 987-3000 x5676, harell.allison@uqam.ca
 Peter Loewen, PhD, Political Science, Munk School of Global Affairs, University of Toronto,
(416) 978-5120, peter.loewen@utoronto.ca
 Daniel Rubenson, PhD, Politics and Public Administration, Ryerson University, (416) 979-5000
x 4052, rubenson@ryerson.ca
 Funding: This project is funded by the Social Sciences and Humanities Research Council of
Canada.

 The purpose of this screen is to provide you with information about the research study you are
being invited to participate in. You must be 18 years of age or older and a legal resident of
Canada to be eligible to participate. You are being contacted because you completed a previous
survey in this project.

 The purpose of the study is to obtain information about your views regarding current events,
elections and democracy. Your participation in this study is voluntary. You may decide not to be
in this study. Even if you consent to participate you have the right to not answer individual
questions or to withdraw from the study at any time. If you choose not to participate or to leave
the study at any time it will have no effect on you. If you decide to withdraw from the study, you
may do so at any time by exiting the survey window. Due to the anonymous nature of your data,
once your survey responses have been submitted, the researchers will be unable to withdraw
your data.

 Your survey responses will be collected anonymously through a secure online survey platform
called Qualtrics. Qualtrics uses encryption technology and restricted access authorizations to
protect all data collected. In addition, Western’s Qualtrics server is in Ireland, where privacy
standards are maintained under the European Union safe harbor framework. The data will then
be exported from Qualtrics and securely stored on Western University's server.

 The survey you are being asked to complete today will take about 20 minutes to
complete. Should you complete today’s survey, you may be re-contacted and asked to
participate in additional surveys as well. Participation today does not commit you to complete
any additional surveys.

 The benefit of participating in our study is that your responses will help us to know more about
democracy in Canada. You may not benefit personally from your participation. There are no
known risks or discomforts associated with participating in this study.

We do not offer any compensation for your participation, however if you are eligible to
participate and submit the survey then you may be eligible for compensation from Qualtrics, as
determined by their current policies.


                                                                                              283
 Your confidentiality will be maintained at all times. Representatives of Western University’s
Non-Medical Research Ethics Board may require access to your study-related records to
monitor the conduct of the research. The data will be stored on a secure server at Western
University and will be retained for a minimum of 7 years. Your data may be archived and
retained indefinitely and could be used for future research purposes (e.g., to answer a new
research question). By consenting to participate in this study, you are agreeing that your data
can be used beyond the purposes of this present study by either the current or other
researchers.

 All identifiable information will be deleted from the dataset collected so that individual
participants’ anonymity will be protected. The de-identified data will be accessible by the study
investigators as well as the broader scientific community. More specifically, the data will be
made publicly available so that data may be inspected and analyzed by others. The data that
will be shared in the dataset will not contain any information that can identify you.

You do not waive any legal right by participating in this study.

If you have questions at any time about the study or its results, you may contact:
Dr. Laura Stephenson
Department of Political Science
University of Western Ontario
London, Ontario, Canada
1-519-661-2111 ext. 85164
Laura.stephenson@uwo.ca

 If you have any questions about your rights as a research participant or the conduct of this
study, you may contact The Office of Human Research Ethics (519) 661-3036, 1-844-720-9816,
email: ethics@uwo.ca. This office oversees the ethical conduct of research studies and is not
part of the study team. Everything that you discuss will be kept confidential.

Completion of the survey indicates your consent to participate.

 If you wish to participate in this phase of the study, please close this window and click the
forward arrow to begin the survey.

additional_consent
Lettre d’information et de consentement - Informations supplémentaires
Titre du projet: Étude électorale canadienne 2019
Chercheure principale: Laura Stephenson, PhD, Science politique, University of Western
Ontario, (519) 661-2111x85164, laura.stephenson@uwo.ca
Co-chercheurs: Allison Harell, PhD, Science politique, Université de Québec à Montréal, (514)
987-3000 x5676, harell.allison@uqam.ca
Peter Loewen, PhD, Science politique, Munk School of Global Affairs and Public Policy,


                                                                                                 284
University of Toronto, (416) 978-5120, peter.loewen@utoronto.ca
Daniel Rubenson, PhD, Politiques et administration publique, Ryerson University, (416) 979-
5000 x 4052, rubenson@ryerson.ca
Financement: Ce projet a été financé par le Conseil de recherche en sciences sociales.

 L’objectif de cette page est de vous fournir de l’information concernant l’étude pour laquelle
vous êtes invité à participer. Vous devez avoir 18 ans ou plus et être un résident légal au
Canada pour être éligible à participer. Vous avez été êtes invité à participer à la présente étude
parce que vous avez déjà participé à un autre sondage dans le cadre de ce projet.

 Le but de cette étude est d’obtenir de l’information sur vos points de vue concernant l’actualité,
les élections et la démocratie au Canada. Votre participation à cette étude est volontaire, donc
vous pouvez décider de ne pas y participer. Même si vous décidez de participer, vous avez le
droit de ne pas répondre à certaines questions ou de vous retirer de l’étude en tout temps. Si
vous n’y participez pas ou décidez de vous y retirer, cette décision n’aura aucune conséquence
pour vous. Si vous décidez de vous retirer, vous pouvez le faire en tout temps simplement en
fermant la page. En raison de la nature anonyme de vos données, une fois que vos réponses
au sondage auront été soumises, les chercheurs ne pourront pas retirer vos données.


 Vos réponses seront recueillies de manière anonyme via une plateforme d’enquête en ligne
sécurisée. Cette plateforme, Qualtrics, utilise une technologie de cryptage et des accès
restreints par autorisation pour protéger les données. De plus, le serveur Western de Qualtrics
se retrouve en Irlande, un pays où les standards pour la protection de la vie privée sont établis
sous le bouclier de l’Union européenne. Les données seront ensuite exportées de Qualtrics et
stockées de manière sécurisée sur le serveur de Western University.

 Ce sondage devrait prendre environ 20 minutes à compléter. Si vous participez aujourd’hui, il
est possible que vous soyez recontacté à une date ultérieure et invité à remplir d’autres
sondages. Votre participation aujourd’hui ne vous engage pas à compléter les autres
sondages.

 L’avantage de participer à la présente étude est que vos réponses nous aideront à mieux
comprendre la démocratie au Canada. Vous ne pouvez pas bénéficier personnellement de
votre participation. Il n’y a pas de risques ou d’inconforts liés à votre participation à cette étude.


 Nous n’offrons aucune compensation pour votre participation aujourd’hui. Cependant, si vous
êtes éligible à participer et à soumettre le sondage, vous pourriez être éligible à une
indemnisation de la part de Qualtrics, tel que déterminé par leurs politiques en vigueur.

 Votre confidentialité sera maintenue en tout temps. Les représentants du comité d’éthique de la
recherche non médicale de Western University peuvent avoir besoin d’accéder à vos dossiers
en lien avec l’étude afin de suivre la conduite de la recherche. Les données seront stockées sur


                                                                                                   285
un serveur sécurisé de Western University et seront conservées pendant au moins 7 ans. Vos
données peuvent être archivées et conservées indéfiniment et peuvent être utilisées à des fins
de recherche future (par exemple, pour répondre à une nouvelle question de recherche). En
consentant à participer à cette étude, vous acceptez que vos données puissent être utilisées
au-delà des objectifs de la présente étude par le chercheur actuel ou par d’autres chercheurs.

 Toutes les informations identifiables seront supprimées de l’ensemble de données collectées
afin que l’anonymat des participants individuels soit protégé. Les données anonymisées seront
accessibles aux chercheurs de l’étude ainsi qu’à la communauté scientifique. De manière plus
spécifique, les données seront rendues publiques afin qu’elles puissent être examinées et
analysées par d’autres. Les données qui seront partagées dans le jeu de données ne
contiendront aucune information permettant de vous identifier.

Vous ne renoncez à aucun droit légal en participant à cette étude.

 Si vous avez des questions portant sur l’étude ou ses résultats, vous pouvez contacter, en tout
temps:

 Dre Laura Stephenson
 Département de science politique
 University of Western OntarioLondon, Ontario, Canada
 1-519-661-2111 ext. 85164
 Laura.stephenson@uwo.ca

 Si vous avez des questions sur vos droits en tant que participant à la recherche ou sur la
conduite de cette étude, vous pouvez contacter le Bureau de l’éthique de la recherche humaine
au (519) 661-3036, 1-844-720-9816, ou par courriel: ethics@uwo.ca. Ce bureau supervise la
conduite éthique d’études en recherche et ne fait pas partie de l’équipe de recherche. Tout ce
dont vous discutez restera confidentiel.

 En répondant à l’enquête, vous indiquez votre consentement à participer.

 Si vous souhaitez participer à cette phase de l’étude, veuillez fermer cette fenêtre et indiquer
votre consentement à remplir le sondage.




Page Break




                                                                                               286
pes19_province In which province or territory are you currently living?

   o Alberta (1)
   o British Columbia (2)
   o Manitoba (3)
   o New Brunswick (4)
   o Newfoundland and Labrador (5)
   o Northwest Territories (6)
   o Nova Scotia (7)
   o Nunavut (8)
   o Ontario (9)
   o Prince Edward Island (10)
   o Quebec (11)
   o Saskatchewan (12)
   o Yukon (13)




                                                                          287
pes19_province Dans quelle province ou quel territoire habitez-vous actuellement?

   o Alberta (1)
   o Colombie-Britannique (2)
   o Manitoba (3)
   o Nouveau-Brunswick (4)
   o Terre-Neuve-et-Labrador (5)
   o Territoires du Nord-Ouest (6)
   o Nouvelle-Écosse (7)
   o Nunavut (8)
   o Ontario (9)
   o Île-du-Prince-Édouard (10)
   o Québec (11)
   o Saskatchewan (12)
   o Yukon (13)
Page Break




                                                                                    288
Display This Question:
        If In which province or territory are you currently living? = Ontario
        And Quota white_farney_module_on_toronto Has Not Been Met
Or If
        In which province or territory are you currently living? = Quebec
        And Quota white_farney_module_qb_fr_montreal Has Not Been Met
Or If
        In which province or territory are you currently living? = British Columbia
        And Quota white_farney_module_bc_vancouver Has Not Been Met




pes19_postalcode Please enter your six-digit postal code in the box below. (For example "A1A
1A1", with letters in uppercase)

Your postal code will not be released publicly or shared with any third party.


        ________________________________________________________________

pes19_postalcode Veuillez inscrire votre code postal à six chiffres dans la case ci-dessous. (Par
exemple, "A1A 1A1", avec des lettres majuscules)

Votre code postal ne sera pas divulgué publiquement ni partagé avec des tiers.


        ________________________________________________________________


NOTE: Respondents’ full 6-digit postal code was collected, and used to
determine their riding, but not distributed with the data. The first
three digits of their postal code are available however, in the
variable cps19_fsa (available upon request).



Page Break




                                                                                             289
pes19_citizen Are you a...

   o Canadian citizen (1)
   o Permanent resident (2)
   o Other (3)
pes19_citizen Êtes-vous...

   o Citoyen canadien (1)
   o Résident permanent (2)
   o Autre (3)
NOTE: Respondents who responded with an “Other” citizenship were
screened out of the survey.


End of Block: Consent and basic demographics



   9.3.2       Main issue of campaign
Start of Block: Main issue


pes19_mostimpissue Now we'd like to ask you some questions about the recent federal
election. What was the main issue in the campaign?

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

pes19_mostimpissue Maintenant, nous aimerions vous poser quelques questions sur l'élection
fédérale qui a eu lieu récemment. Quel était l'enjeu principal de la campagne?

Si vous ne le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →

    ________________________________________________________________


End of Block: Main issue



                                                                                       290
   9.3.3        Voting: turnout
Start of Block: Voting part 1 - turnout
Display This Question:
    If Are you a... = Canadian citizen


pes19_turnout2019 The federal election was held on Monday, October 21. In any election,
some people are not able to vote because they are sick or busy, or for some other reason.
Others do not want to vote. Did you vote in the recent federal election?

   o Yes (1)
   o No (2)
   o I usually vote but didn't this time (5)
   o I thought about voting but didn't (6)
   o I wasn’t registered to vote (3)
   o Don't know/ Don't remember (4)
   o Prefer not to answer (8)
pes19_turnout2019 Les élections fédérales ont eu lieu le lundi 21 octobre. Dans toute élection,
certaines personnes sont dans l’incapacité de voter parce qu’elles sont malades ou occupées,




                                                                                            291
ou pour toute autre raison. D'autres personnes ne veulent pas voter. Avez-vous voté lors de
l'élection fédérale la plus récente?

   o Oui (1)
   o Non (2)
   o Je vote habituellement mais je ne l'ai pas fait cette fois-ci (5)
   o J'ai pensé à voter mais je ne l'ai pas fait (6)
   o Je ne suis pas enregistré(e) pour voter (3)
   o Je ne sais pas / Je ne m'en souviens pas (4)
   o Préfère ne pas répondre (8)
Display This Question:
    If Are you a... = Canadian citizen


pes19_turnout2019_v2 The federal election was held on Monday, October 21. In any election,
some people are not able to vote because they are sick or busy, or for some other reason.
Others do not want to vote. Did you vote in the recent federal election?

   o Yes (1)
   o No (2)
   o Don't know/ Don't remember (4)
   o Prefer not to answer (3)
pes19_turnout2019_v2 Les élections fédérales ont eu lieu le lundi 21 octobre. Dans toute
élection, certaines personnes sont dans l’incapacité de voter parce qu’elles sont malades ou




                                                                                               292
occupées, ou pour toute autre raison. D'autres personnes ne veulent pas voter. Avez-vous voté
lors de l'élection fédérale la plus récente?

    o Oui (1)
    o Non (2)
    o Je ne sais pas/ Je ne m'en souviens pas (4)
    o Préfère ne pas répondre (3)
End of Block: Voting part 1 - turnout



    9.3.4       Voting: reasons and method

NOTE: There was a question type experiment for reasons for not voting.
notvote_split was randomly set to either “categorical” or “textbox”.
If notvote_split was “categorical” (and the respondent did not vote),
the respondent received the question pes19_notvotereason1, which was a
categorical question listing potential reasons why they did not vote
and asking them to select the main reason. If notvote_split was
“textbox” (and the respondent did not vote), the respondent received
the question pes19_notvotereason2, which provided a text box for the
respondent to write in the main reason why they did not vote.


Start of Block: Voting part 2 - Reason for voting or not voting
Display This Question:
      If The federal election was held on Monday, October 21. In any election, some people are not able
to... = No
      Or The federal election was held on Monday, October 21. In any election, some people are not able
to... = I usually vote but didn't this time
      Or The federal election was held on Monday, October 21. In any election, some people are not able
to... = I thought about voting but didn't
      Or The federal election was held on Monday, October 21. In any election, some people are not able
to... = I wasn’t registered to vote
      Or The federal election was held on Monday, October 21. In any election, some people are not able
to... = No
And If
    notvote_split = categorical




                                                                                                     293
pes19_notvotereason1 What is the main reason you did not vote?

   o My vote will not make a difference, nothing will change, etc. (1)
   o No time, too busy, etc. (2)
   o No interest, did not follow election or issues, etc. (3)
   o Physical limitations, mobility issues, sick/ill, aged, etc. (4)
   o Not able to prove ID or address (5)
   o Did not know when / where to vote (6)
   o Don't know/ Prefer not to answer (7)
pes19_notvotereason1 Quelle est la raison principale qui explique pourquoi vous n'avez pas
voté?

   o Mon vote ne fera aucune différence, rien ne va changer (1)
   o Pas le temps, trop occupé(e) (2)
   o Pas d'intérêt, je n'ai pas suivi les élections ou les enjeux (3)
   o Limitations physiques, problèmes de mobilité, malade, âge (4)
   o Impossible de valider mon identité ou mon adresse (5)
   o Je ne savais pas quand / où voter (6)
   o Je ne sais pas / Préfère ne pas répondre (7)
Page Break




                                                                                             294
Display This Question:
      If The federal election was held on Monday, October 21. In any election, some people are not able
to... = No
      Or The federal election was held on Monday, October 21. In any election, some people are not able
to... = I usually vote but didn't this time
      Or The federal election was held on Monday, October 21. In any election, some people are not able
to... = I thought about voting but didn't
      Or The federal election was held on Monday, October 21. In any election, some people are not able
to... = I wasn’t registered to vote
      Or The federal election was held on Monday, October 21. In any election, some people are not able
to... = No
And If
    notvote_split = textbox


pes19_notvotereason2 What is the main reason you did not vote?

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

pes19_notvotereason2 Quelle est la raison principale pour laquelle vous n'avez pas voté?


Si vous ne le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →

    ________________________________________________________________



Page Break




                                                                                                     295
Display This Question:
      If The federal election was held on Monday, October 21. In any election, some people are not able
to... = Yes
      Or The federal election was held on Monday, October 21. In any election, some people are not able
to... = Yes


pes19_howvote There are many options for people wanting to vote in an election. How did you
vote?

    o At a polling station on election day, October 21 (1)
    o At an advance polling station (or advance polls) (2)
    o At a local Elections Canada office (3)
    o By mail (4)
    o At home (5)
    o On campus (6)
    o Other (please specify) (7) ________________________________________________
    o Don't know/ Prefer not to answer (8)




                                                                                                     296
pes19_howvote Il existe de nombreuses options pour les personnes souhaitant voter lors d'une
élection. Comment avez-vous voté?

   o Le jour du scrutin, le 21 octobre, au bureau de vote (1)
   o Au bureau de vote par anticipation (vote par anticipation) (2)
   o Dans un bureau local d'Élections Canada (3)
   o Par la poste (4)
   o À la maison (5)
   o Sur mon campus (6)
   o Autre (veuillez préciser) (7) ________________________________________________
   o Je ne sais pas / Préfère ne pas répondre (8)
Page Break




                                                                                         297
Display This Question:
      If The federal election was held on Monday, October 21. In any election, some people are not able
to... = Yes
      Or The federal election was held on Monday, October 21. In any election, some people are not able
to... = Yes


pes19_votereason Did you vote mainly because...

    o It was your duty (1)
    o Your vote could make a difference (2)
    o You liked a particular party, leader or candidate (3)
    o Don't know/ Prefer not to answer (4)
pes19_votereason Avez-vous voté surtout parce que ...

    o C'était votre devoir (1)
    o Votre vote pourrait faire une différence (2)
    o Vous aimiez un parti, un chef ou un candidat en particulier (3)
    o Je ne sais pas / Préfère ne pas répondre (4)
End of Block: Voting part 2 - Reason for voting or not voting



    9.3.5       Voting: vote choice


NOTE: From October 24 to 27, the display logic for
pes19_votechoice2019 was set to AND, which was impossible to fulfill,
thus preventing any respondents from receiving this question. It
affected 953 respondents who were intended to have received the
question but did not. This was fixed on October 27, 2019, at 1:04pm
EST.


Start of Block: Voting part 2 -vote choice




                                                                                                     298
Display This Question:
      If The federal election was held on Monday, October 21. In any election, some people are not able
to... = Yes
      Or The federal election was held on Monday, October 21. In any election, some people are not able
to... = Yes




pes19_votechoice2019 Which party did you vote for?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
In which province or territory are you currently living? = Quebec

    o Bloc Québécois (4)
    o Green Party (5)
    o People's Party (6)
    o Another party (specify) (7) ________________________________________________
    o I spoiled my vote (8)
    o Don't know / Prefer not to answer (9)




                                                                                                     299
pes19_votechoice2019 Pour quel parti avez-vous voté?

    o Le Parti libéral (1)
    o Le Parti conservateur (2)
    o Le NPD (3)
In which province or territory are you currently living? = Quebec

    o Le Bloc québécois (4)
    o Le Parti vert (5)
    o Le Parti populaire (6)
    o Un autre parti (spécifiez) (7)
    ________________________________________________

    o J'ai annulé mon vote (8)
    o Je ne sais pas / Préfère ne pas répondre (9)
Display This Question:
    If Are you a... = Permanent resident




                                                                    300
pes19_pr_votechoice If you could have voted in the federal election on Oct. 21, which party
would you have voted for?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
In which province or territory are you currently living? = Quebec

    o Bloc Québécois (4)
    o Green Party (5)
    o People's Party (6)
    o Another party (specify) (7) ________________________________________________
    o I would have spoiled my vote (8)
    o Don't know / Prefer not to answer (9)




                                                                                              301
pes19_pr_votechoice Si vous auriez pu voter lors de l'élection fédérale du 21 octobre, pour quel
parti auriez-vous voté?

    o Le Parti libéral (1)
    o Le Parti conservateur (2)
    o Le NPD (3)
In which province or territory are you currently living? = Quebec

    o Le Bloc québécois (4)
    o Le Parti vert (5)
    o Le Parti populaire (6)
    o Un autre parti (spécifiez) (7)
    ________________________________________________

    o J'ai annulé mon vote (8)
    o Je ne sais pas / Préfère ne pas répondre (9)
End of Block: Voting part 2 -vote choice




                                                                                            302
   9.3.6       Satisfaction with democracy
Start of Block: Satisfaction with democracy


pes19_dem_sat On the whole, are you very satisfied, fairly satisfied, not very satisfied, or not
satisfied at all with the way democracy works in Canada?

   o Very satisfied (1)
   o Fairly satisfied (2)
   o Not very satisfied (3)
   o Not satisfied at all (4)
   o Don't know / Prefer not to answer (5)
pes19_dem_sat Dans l’ensemble, êtes-vous très satisfait, assez satisfait, pas très satisfait ou
pas du tout satisfait du fonctionnement de la démocratie au Canada?

   o Très satisfait (1)
   o Plutôt satisfait (2)
   o Pas très satisfait (3)
   o Pas du tout satisfait (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
End of Block: Satisfaction with democracy




                                                                                               303
   9.3.7      Attention to campaign
Start of Block: Attention to campaign


pes19_campatt How much attention did you pay to the election campaign?

   o A lot (1)
   o Some (2)
   o Not much at all (3)
   o Don't know/ Prefer not to answer (4)
pes19_campatt Combien d'attention avez-vous portée à la campagne électorale?

   o Beaucoup (1)
   o Un peu (2)
   o Pas beaucoup (3)
   o Je ne sais pas / Préfère ne pas répondre (4)
End of Block: Attention to campaign



   9.3.8      Party contact
Start of Block: Parties contacted


pes19_contact1 During the campaign, did a party or candidate contact you in person or by any
other means?

   o Yes (1)
   o No (2)
   o Don't know/ Prefer not to answer (3)


                                                                                          304
pes19_contact1 Durant la campagne, est-ce qu’un parti ou un candidat vous a contacté en
personne ou de toute autre façon?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)
Page Break




                                                                                          305
Display This Question:
    If During the campaign, did a party or candidate contact you in person or by any other means? = Yes




pes19_contact2 Do you recall which parties or candidates contacted you? (Please select all that
that apply)


    ▢           Liberal Party (1)


    ▢           Conservative Party (2)


    ▢           NDP (3)
In which province or territory are you currently living? = Quebec


    ▢           Bloc Québécois (4)


    ▢           Green Party (5)


    ▢           People's Party (8)


    ▢        Another party (please specify) (6)
    ________________________________________________


    ▢           Don’t know/ Prefer not to answer (7)




                                                                                                   306
pes19_contact2 Durant la campagne électorale, quel parti ou candidat vous a contacté?
(Veuillez sélectionner tous ceux qui s'appliquent)


    ▢           Parti libéral (1)


    ▢           Parti conservateur (2)


    ▢           Nouveau Parti démocratique (3)
In which province or territory are you currently living? = Quebec


    ▢           Bloc québécois (4)


    ▢           Parti vert (5)


    ▢           Parti populaire du Canada (8)


    ▢        Un autre parti (veuillez préciser) (6)
    ________________________________________________


    ▢           Je ne sais pas / Préfère ne pas répondre (7)


End of Block: Parties contacted



    9.3.9       Mandate
Start of Block: Legitimate mandate




                                                                                        307
pes19_mandate Given the results of the October 21 election, does the winning party have a
legitimate mandate to implement its policies?

   o Yes (1)
   o No (2)
   o Don’t know/ Prefer not to answer (3)
pes19_mandate Compte tenu des résultats de l'élection du 21 octobre, le parti gagnant a-t-il un
mandat légitime pour mettre en œuvre ses politiques?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)
End of Block: Legitimate mandate



   9.3.10     Government formation
Start of Block: Government formation

pes19_formgovt Which should be more important to forming the government in Canada:

   o Winning the most seats (1)
   o Winning the most votes (2)
   o Don’t know/ Prefer not to answer (3)




                                                                                            308
pes19_formgovt Qu'est-ce qui devrait être le plus important pour former le gouvernement au
Canada:

   o Gagner le plus de sièges (1)
   o Gagner le plus de votes (2)
   o Je ne sais pas/Préfère ne pas répondre (3)
End of Block: Government formation




                                                                                             309
   9.3.11     Party promises
Start of Block: Parties keep promises


pes19_keepromises Do political parties keep their election promises:

   o Most of the time (1)
   o Some of the time (2)
   o Hardly ever (3)
   o Never (4)
   o Depends on the party (5)
   o Don't know/ Prefer not to answer (6)
pes19_keepromises Les partis politiques tiennent-ils leurs promesses électorales:

   o La plupart du temps (1)
   o Une partie du temps (2)
   o Presque jamais (3)
   o Jamais (4)
   o Cela dépend du parti (5)
   o Je ne sais pas / Préfère ne pas répondre (6)
End of Block: Parties keep promises




                                                                                    310
   9.3.12      Group thermometers
Start of Block: Groups thermometers




pes19_groups1 How do you feel about the following groups? Set the slider to any number from
0 to 100, where 0 means you really dislike the group and 100 means you really like the group.

If you do not know, or prefer not to answer, please click →
                                                  Really dislike   Really like   Don't know/
                                                                                 Prefer not to
                                                                                   answer

                                                  0   10 20 30 40 50 60 70 80 90 100

             Aboriginal Peoples ()

             Gays and Lesbians ()

          Muslims Living in Canada ()

            Politicians in General ()




pes19_groups1 Que pensez-vous des différents groupes ci-dessous? Veuillez glisser la barre
sur un chiffre entre 0 et 100, où 0 indique que vous n'aimez vraiment pas du tout le groupe et
100 que vous aimez vraiment beaucoup ce groupe.


Si vous ne savez pas, ou préférez ne pas répondre, veuillez sélectionner →
                                                 Je n'aime     J'aime vraiment Je ne sais
                                              vraiment pas du beaucoup        pas/préfère ne
                                                    tout                       pas répondre

                                                  0   10 20 30 40 50 60 70 80 90 100




                                                                                           311
          Les peuples autochtones ()

            Les gais et lesbiennes ()

     Les Musulmans vivant au Canada ()

          Les politiciens en général ()




End of Block: Groups thermometers



   9.3.13      Party words


NOTE: Respondents were asked about ONE randomly-selected party. The
Bloc Quebecois were only a potential selection for respondents in
Quebec.


Start of Block: Few words on each party - Liberal Party


pes19_libwords In a few words, what come to mind immediately when you think about
the Liberal Party ?


If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

pes19_libwords En quelques mots, décrivez ce qui vous vient en tête spontanément lorsque
vous pensez au Parti libéral?


Si vous ne le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →

    ________________________________________________________________

End of Block: Few words on each party - Liberal Party

Start of Block: Few words on each party - Conservative Party




                                                                                           312
pes19_conwords In a few words, what come to mind immediately when you think about
the Conservative Party?


If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

pes19_conwords En quelques mots, décrivez ce qui vous vient en tête spontanément lorsque
vous pensez au Parti conservateur?


Si vous ne le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →

    ________________________________________________________________


End of Block: Few words on each party - Conservative Party

Start of Block: Few words on each party - New Democratic Party


pes19_ndpwords In a few words, what come to mind immediately when you think about the
New Democratic Party?
 If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

pes19_ndpwords En quelques mots, décrivez ce qui vous vient en tête spontanément lorsque
vous pensez au Nouveau Parti démocratique?


Si vous ne le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →

    ________________________________________________________________


End of Block: Few words on each party - New Democratic Party

Start of Block: Few words on each party - Bloc Quebecois


pes19_bqwords In a few words, what come to mind immediately when you think about the Bloc
Québécois?

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________


                                                                                        313
pes19_bqwords En quelques mots, décrivez ce qui vous vient en tête spontanément lorsque
vous pensez au Bloc québécois?


Si vous ne le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →

    ________________________________________________________________


End of Block: Few words on each party - Bloc Quebecois

Start of Block: Few words on each party - Green Party


pes19_greenwords In a few words, what come to mind immediately when you think about the
Green Party?

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

pes19_greenwords En quelques mots, décrivez ce qui vous vient en tête spontanément lorsque
vous pensez au Parti vert?


Si vous ne le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →

    ________________________________________________________________


End of Block: Few words on each party - Green Party

Start of Block: Few words on each party - People's Party


pes19_peopleswords In a few words, what come to mind immediately when you think about the
People's Party?

If you do not know, or prefer not to answer, please click →

    ________________________________________________________________

pes19_peopleswords En quelques mots, décrivez ce qui vous vient en tête spontanément
lorsque vous pensez au Parti populaire?




                                                                                          314
Si vous ne le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →

    ________________________________________________________________


End of Block: Few words on each party - People's Party



   9.3.14     Economy
Start of Block: Retrospective state of the economy


pes19_econ_retro Would you say that over the past twelve months, the state of the economy in
Canada has gotten...

   o Much better (1)
   o Somewhat better (2)
   o Stayed about the same (3)
   o Somewhat worse (4)
   o Much worse (5)
   o Don't know/ Prefer not to answer (6)
pes19_econ_retro Diriez-vous qu’au courant des douze derniers mois, l'économie au Canada...

   o S'est beaucoup améliorée (1)
   o S'est un peu améliorée (2)
   o Est restée à peu près la même (3)
   o S'est un peu détériorée (4)
   o S'est beaucoup détériorée (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)

                                                                                         315
End of Block: Retrospective state of the economy



   9.3.15     Electoral reform
Start of Block: Likert section 1 intro


pes19_likert_intro1 How much do you agree or disagree with the following statements? Please
click → to see first statement.

pes19_likert_intro1 À quel point êtes-vous en accord ou en désaccord avec les énoncés
suivants? Cliquez → pour voir le premier énoncé.


End of Block: Likert section 1 intro

Start of Block: Statement: electoral reform


pes19_pos_fptp Canada should change its electoral system from “First Past the Post” to a
“proportional representation” system.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                           316
pes19_pos_fptp
Le Canada devrait changer son système électoral afin de passer du mode de scrutin actuel à un
système de "représentation proportionnelle".

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Statement: electoral reform




                                                                                         317
   9.3.16     Paid medical treatment


NOTE: pes19_paymed was set to receive a split sample of 50% (1/2), to
make room in the survey for more questions. Whether a respondent was
assigned to receive pes19_paymed was randomly determined in the Survey
Flow by setting the embedded data field split_medical to either 0 or
1. If split_medical was equal to 1, they were assigned to receive
pes19_paymed. split_medical can be used to filter the dataset to only
respondents that were assigned to receive pes19_paymed.


Start of Block: Position statements: Paid medical treatment


pes19_paymed People who are willing to pay should be allowed to get medical treatment
sooner.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                        318
pes19_paymed Les personnes disposées à payer devraient pouvoir obtenir des traitements
médicaux plus tôt.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Position statements: Paid medical treatment




                                                                                         319
   9.3.17    Senate

NOTE: pes19_senate was set to receive a split sample of 50% (1/2), to
make room in the survey for more questions. Whether a respondent was
assigned to receive pes19_senate was randomly determined in the Survey
Flow by setting the embedded data field split_senate to either 0 or 1.
If split_senate was equal to 1, they were assigned to receive
pes19_senate. split_senate can be used to filter the dataset to only
respondents that were assigned to receive pes19_senate.


Start of Block: Other: statements: Senate


pes19_senate The Senate should be abolished.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                    320
pes19_senate
Le Sénat devrait être aboli.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Other: statements: Senate



   9.3.18      Environment versus jobs
Start of Block: Issue positions - environment versus jobs




pes19_envirojob When there is a conflict between protecting the environment and creating
jobs, jobs should come first.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)

                                                                                           321
pes19_envirojob Lorsqu'il existe un conflit entre la protection de l'environnement et la création
d'emplois, les emplois devraient avoir la priorité.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Issue positions - environment versus jobs




                                                                                               322
   9.3.19      Democratic values

NOTE: The order of pes19_hatespeech, pes19_losetouch, and
pes19_womenhome was randomized.

   4.1.1.1     Hate speech


NOTE: pes19_hatespeech was set to receive a split sample of 50% (1/2),
to make room in the survey for more questions. Whether a respondent
was assigned to receive pes19_hatespeech was randomly determined in
the Survey Flow by setting the embedded data field split_hatespeech to
either 0 or 1. If split_hatespeech was equal to 1, they were assigned
to receive pes19_hatespeech. split_hatespeech can be used to filter
the dataset to only respondents that were assigned to receive
pes19_hatespeech.


Start of Block: Democracy Checkup - democratic values: hate speech

pes19_hatespeech It should be illegal to say hateful things publicly about racial, ethnic and
religious groups.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                                323
pes19_hatespeech
Tenir des propos haineux à l'égard de groupes raciaux, ethniques et religieux devrait être
illégal.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - democratic values: hate speech



   4.1.1.2    Lose touch
Start of Block: Democracy Checkup - democratic values: lose touch


pes19_losetouch Those elected to Parliament soon lose touch with the people.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)



                                                                                             324
pes19_losetouch
Ceux qui sont élus au Parlement perdent vite contact avec la population.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - democratic values: lose touch



   4.1.1.3    Women home
Start of Block: Democracy Checkup - democratic values: women home


pes19_womenhome Society would be better off if fewer women worked outside the home.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                      325
pes19_womenhome
La société se porterait mieux si moins de femmes travaillaient à l'extérieur du foyer.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - democratic values: women home



   9.3.20      Efficacy

NOTE: The order of the efficacy questions, pes19_govtcare,
pes19_complicated, and pes19_famvalues, was randomized.
Start of Block: Democracy Checkup - efficacy and government: govt care


pes19_govtcare The government does not care much about what people like me think.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)


                                                                                         326
pes19_govtcare Le gouvernement ne se soucie pas beaucoup de ce que les gens comme moi
pensent.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - efficacy and government: govt care

Start of Block: Efficacy - understand




pes19_complicated Sometimes, politics and government seem so complicated that a person
like me can't really understand what's going on.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)



                                                                                         327
pes19_complicated
Parfois la politique et le gouvernement semblent si compliqués qu'une personne comme moi ne
peut pas vraiment comprendre ce qui se passe.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Efficacy - understand

Start of Block: Democracy Checkup - efficacy and government: family values


pes19_famvalues This country would have many fewer problems if there was more emphasis
on traditional family values.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                        328
pes19_famvalues Il y aurait moins de problèmes dans ce pays si on accordait plus d’importance
aux valeurs familiales traditionnelles.

    o Fortement en désaccord (1)
    o Plutôt en désaccord (2)
    o Ni en accord, ni en désaccord (3)
    o Plutôt en accord (4)
    o Fortement en accord (5)
    o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - efficacy and government: family values



   9.3.21       Politician lies, bilingualism, and equal rights

NOTE: Respondents received either pes19_pollie, OR pes19_bilingualism
and pes19_equalrights. The order of pes19_bilingualism and
pes19_equalrights was randomized if they received them.
Start of Block: Democracy Checkup - democratic values: politicians lie


pes19_pollie Politicians are willing to lie to get elected.

    o Strongly disagree (1)
    o Somewhat disagree (2)
    o Neither agree nor disagree (3)
    o Somewhat agree (4)
    o Strongly agree (5)
    o Don't know/ Prefer not to answer (6)

                                                                                         329
pes19_pollie
Les politiciens sont prêts à mentir pour se faire élire.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - democratic values: politicians lie

Start of Block: Democracy Checkup - attitudes towards diversity: bilingualism


pes19_bilingualism We have gone too far in pushing bilingualism in Canada.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                330
pes19_bilingualism
Nous sommes allés trop loin dans la promotion du bilinguisme au Canada.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - attitudes towards diversity: bilingualism

Start of Block: Democracy Checkup - democratic values: equal rights


pes19_equalrights We have gone too far in pushing equal rights in this country.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                  331
pes19_equalrights
On est allé trop loin dans la promotion des droits égaux dans ce pays.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - democratic values: equal rights



   9.3.22     Group identity
Start of Block: Democracy Checkup - attitudes towards diversity: group identity


pes19_ethid My ethnicity and language are important parts of my identity.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                  332
pes19_ethid Mon origine ethnique et ma langue sont des éléments importants de mon identité.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - attitudes towards diversity: group identity




                                                                                        333
   9.3.23      Assimilation and immigrants taking jobs

NOTE: pes19_fitin and pes19_immigjobs were set to receive a split
sample of 50% (1/2), to make room in the survey for more questions.
Whether a respondent was assigned to receive pes19_fitin and
pes19_immigjobs was randomly determined in the Survey Flow by setting
the embedded data field split_att_div to either 0 or 1. If
split_att_div was equal to 1, they were assigned to receive
pes19_fitin and pes19_immigjobs. split_att_div can be used to filter
the dataset to only respondents that were assigned to receive
pes19_fitin and pes19_immigjobs.

Also note that the order of these two questions was randomized.


Start of Block: Democracy Checkup - attitudes towards diversity: assimilation


pes19_fitin Too many recent immigrants just don't want to fit in to Canadian society.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                        334
pes19_fitin
Un trop grand nombre d’immigrants récents ne veulent tout simplement pas s'intégrer.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - attitudes towards diversity: assimilation

Start of Block: Democracy Checkup - attitudes towards diversity: take jobs


pes19_immigjobs Immigrants take jobs away from other Canadians.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                       335
pes19_immigjobs
Les immigrants enlèvent des emplois aux autres Canadiens.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - attitudes towards diversity: take jobs




                                                                           336
   9.3.24     Government effectiveness and programs

NOTE: pes19_govteff and pes19_govtprograms were set to receive a split
sample of 50% (1/2), to make room in the survey for more questions.
Whether a respondent was assigned to receive pes19_govteff and
pes19_govtprograms was randomly determined in the Survey Flow by
setting the embedded data field split_govt_eff to either 0 or 1. If
split_govt_eff was equal to 1, they were assigned to receive
pes19_govteff and pes19_govtprograms. split_govt_eff can be used to
filter the dataset to only respondents that were assigned to receive
pes19_govteff and pes19_govtprograms.

Also note that the order of these two questions was randomized.


Start of Block: Democracy Checkup - efficacy and government: govt effectiveness


pes19_govteff Governments used to be better at getting things done.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                  337
pes19_govteff Les gouvernements étaient plus efficaces dans le passé.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - efficacy and government: govt effectiveness




                                                                                338
Start of Block: Democracy Checkup - efficacy and government: govt programs


pes19_govtprograms Government can no longer ${e://Field/govt_programs_word} the kinds of
programs and services people want.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_govtprograms
Le gouvernement ${e://Field/govt_programs_word_fr} les programmes et les services que les
gens désirent.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Democracy Checkup - efficacy and government: govt programs




                                                                                        339
   9.3.25     Ties with US and China and country thermometers

NOTE: pes19_tieus, pes19_tiechina, and pes19_country were set to
receive a split sample of 50% (1/2), to make room in the survey for
more questions. Whether a respondent was assigned to receive
pes19_tieus, pes19_tiechina, and pes19_country was randomly determined
in the Survey Flow by setting the embedded data field split_ties to
either 0 or 1. If split_ties was equal to 1, they were assigned to
receive pes19_tieus, pes19_tiechina, and pes19_country. split_ties can
be used to filter the dataset to only respondents that were assigned
to receive pes19_tieus, pes19_tiechina, and pes19_country.

Also note that the order of pes19_tieus and pes19_tiechina was
randomized.


Start of Block: Democracy Checkup: ties with US


pes19_tieus Do you think Canada's ties with the United States should be...

   o Much closer (1)
   o Somewhat closer (2)
   o About the same as now (3)
   o Somewhat more distant (4)
   o Much more distant (5)
   o Don't know/ Prefer not to answer (6)




                                                                             340
pes19_tieus Croyez-vous que les liens entre le Canada et les États-Unis devraient être...

   o Beaucoup plus serrés (1)
   o Assez serrés (2)
   o A peu près les mêmes que maintenant (3)
   o Un peu plus distants (4)
   o Beaucoup plus distants (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Democracy Checkup: ties with US

Start of Block: Democracy Checkup: ties with China


pes19_tiechina Do you think Canada's ties with China should be...

   o Much closer (1)
   o Somewhat closer (2)
   o About the same as now (3)
   o Somewhat more distant (4)
   o Much more distant (5)
   o Don't know/ Prefer not to answer (6)




                                                                                            341
pes19_tiechina Croyez-vous que les liens entre le Canada et la Chine devraient être...

   o Beaucoup plus serrés (1)
   o Assez serrés (2)
   o Un peu près les mêmes que maintenant (3)
   o Un peu plus distants (4)
   o Beaucoup plus distants (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Democracy Checkup: ties with China

Start of Block: Country Thermometers




pes19_country How do you feel about the following countries or places? Set the slider to any
number from 0 to 100, where 0 means you really dislike it and 100 means you really like it.

If you do not know, or prefer not to answer, please click →
                                                  Really dislike   Really like   Don't know/
                                                                                 Prefer not to
                                                                                   answer

                                                  0   10 20 30 40 50 60 70 80 90 100

                   Canada ()

                United States ()

                   Quebec ()

                    China ()




                                                                                           342
pes19_country Que pensez-vous des différents pays ou endroits ci-dessous? Veuillez glisser la
barre sur un chiffre entre 0 et 100, où 0 indique que vous ne les aimez vraiment pas du
tout et 100 que vous les aimez vraiment beaucoup.


Si vous ne savez pas, ou préférez ne pas répondre, veuillez sélectionner →
                                                 Je n'aime     J'aime vraiment Je ne sais
                                              vraiment pas du beaucoup        pas/préfère ne
                                                    tout                       pas répondre

                                                0   10 20 30 40 50 60 70 80 90 100

                Le Canada ()

               Les États-Unis ()

                Le Québec ()

                 La Chine ()




End of Block: Country Thermometers




                                                                                          343
   9.3.26          Comparative Study of Electoral Systems (Module 5) questions

NOTE: There were two large sets of questions, of which the respondent
would receive one: either the Comparative Study of Electoral Systems
(CSES) Module 5 questions, or the questions related to experiences
with the electoral process. The two sets of questions were designed to
take roughly the same amount of time for respondents to complete.


Start of Block: CSES Canadian Identity

pes19_can_id Some people say that the following things are important for being truly Canadian.
Others say they are not important. How important do you think the following is for being truly
Canadian...
                                                                                   Don't know /
                 Not important      Not very        Fairly            Very
                                                                                   Prefer not to
                    at all (1)    important (2) important (3) important (4)
                                                                                    answer (5)
 To have been
    born in
  Canada. (1)              o             o              o               o               o
    For your
 grandparents
 to have been
     born in               o             o              o               o               o
  Canada. (2)
 To be able to
    speak
  English or
  French. (3)
                           o             o              o               o               o
    To follow
   Canada's
 customs and
 traditions. (4)
                           o             o              o               o               o




                                                                                            344
pes19_can_id Certaines personnes disent que les critères qui suivent sont importants pour être
véritablement Canadien(ne). D’autres disent qu’ils ne sont pas importants. Selon vous, quel est
le niveau d’importance de ces critères pour être véritablement canadien(ne)…
                                                                                  Je ne sais
                      Pas
                                   Pas très         Assez           Très         pas/ Préfère
                  important du
                                 important (2)   important (3)   important (4)      ne pas
                    tout (1)
                                                                                 répondre (5)

 D’être né au
 Canada. (1)           o               o               o               o               o
   Que vos
    grands-
    parents
 soient nés au         o               o               o               o               o
  Canada. (2)
     D’être
  capable de
    parler le
  français ou          o               o               o               o               o
 l'anglais. (3)
 De respecter
 les coutumes
      et les
  traditions du        o               o               o               o               o
  Canada. (4)



End of Block: CSES Canadian Identity

Start of Block: CSES questions part 1




                                                                                           345
pes19_ottawa_perf Now thinking about the performance of the government in Ottawa in
general, how good or bad a job do you think the government in Ottawa did over the past four
years?

   o A very good job (1)
   o A good job (2)
   o A bad job (3)
   o A very bad job (4)
   o Don't know / Prefer not to answer (5)
pes19_ottawa_perf Au sujet de la performance générale du gouvernement à Ottawa, à quel
point a-t-il fait un bon ou mauvais travail au cours des quatre dernières années?

   o Un très bon travail (1)
   o Un bon travail (2)
   o Un mauvais travail (3)
   o Un très mauvais travail (4)
   o Je ne sais pas/ Préfère ne pas répondre (5)
Page Break




                                                                                              346
pes19_party_rep Would you say that any of the federal parties in Canada represent your views
reasonably well?

   o Yes (1)
   o No (2)
   o Don't know / Prefer not to answer (3)
pes19_party_rep Diriez-vous que l'un des partis fédéraux au Canada représente assez bien
votre point de vue?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)
Page Break




                                                                                           347
Display This Question:
      If Would you say that any of the federal parties in Canada represent your views reasonably well? =
Yes




pes19_party_rep_whic Which party represents your views best?

      o Conservative Party (1)
      o Liberal Party (2)
      o NDP (3)
      o Green Party (4)
      o People's Party (5)
In which province or territory are you currently living? = Quebec

      o Bloc Québécois (6)
      o Other (specify) (7) ________________________________________________
      o Don't know / Prefer not to say (8)




                                                                                                      348
pes19_party_rep_whic Quel parti représente le mieux vos points de vue?

    o Parti conservateur (1)
    o Parti libéral (2)
    o Nouveau Parti démocratique (NPD) (3)
    o Parti vert (4)
    o Parti populaire (5)
In which province or territory are you currently living? = Quebec

    o Bloc québécois (6)
    o Autre (spécifiez) (7) ________________________________________________
    o Je ne sais pas/ Préfère ne pas répondre (8)
End of Block: CSES questions part 1

Start of Block: CSES parties and leaders - Phone-to-web wording - Parties



pes19_party_rate We’d like to know what you think about each of our political parties. After the
name of a political party, please rate it on a scale from 0 to 10, where 0 means you strongly
dislike that party and 10 means that you strongly like that party. If you come to a party you
haven’t heard of or you feel you do not know enough about, just say so.
                                                   Strongly dislike Strongly like   Don't know/
                                                                                   Prefer not to
                                                                                      answer

                                                       0    1       2   3   4   5   6   7   8   9   10




                                                                                                    349
         Federal Conservative Party ()

            Federal Liberal Party ()

                Federal NDP ()

               Bloc Québécois ()

            Federal Green Party ()




pes19_party_rate Nous aimerions avoir votre opinion sur chacun de nos partis politiques. Dans
chaque cas, veuillez situer le parti politique sur une échelle de 0 à 10, où 0 signifie que vous ne
l’aimez vraiment pas du tout et 10, que vous l'aimez vraiment beaucoup. Si vous arrivez sur
un parti dont vous n’avez pas entendu parler ou bien que vous estimez ne pas en connaître
assez, indiquez-le simplement.
                                                    Aime vraiment Aime vraiment Je ne sais pas/
                                                     pas du tout      beaucoup       Préfère ne pas
                                                                                        répondre

                                                   0   1    2   3    4   5    6   7    8   9   10

          Parti conservateur fédéral ()

             Parti libéral fédéral ()

                 NPD fédéral ()

               Bloc québécois ()

              Parti vert fédéral ()




End of Block: CSES parties and leaders - Phone-to-web wording - Parties

Start of Block: CSES parties and leaders - Phone-to-web wording - Leaders



pes19_lead_rate And what do you think of the party leaders? After the name of a party leader,
please rate them on a scale from 0 to 10, where 0 means you strongly dislike that party leader
and 10 means that you strongly like that party leader. If you come to a party leader you haven’t



                                                                                               350
heard of or you feel you do not know enough about, just say so.

                                                Strongly dislike   Strongly like       Don't know/
                                                                                       Prefer not to
                                                                                         answer

                                                 0    1   2    3    4   5    6     7     8    9   10

               Andrew Scheer ()

               Justin Trudeau ()

               Jagmeet Singh ()

               Elizabeth May ()

          Yves-François Blanchet ()




pes19_lead_rate Et que pensez-vous de chacun des chefs de partis fédéraux? À chaque fois,
veuillez situer le chef sur une échelle de 0 à 10, où 0 signifie que vous ne l’aimez vraiment pas
du tout et 10, que vous l'aimez vraiment beaucoup. Si vous arrivez à un chef de parti dont
vous n’avez pas entendu parler ou bien que vous estimez ne pas en connaître assez sur ce
chef, indiquez-le simplement.
                                                   Aime vraiment Aime vraiment Je ne sais pas/
                                                    pas du tout       beaucoup     Préfère ne pas
                                                                                      répondre

                                                 0    1   2    3    4   5    6     7     8    9   10

               Andrew Scheer ()

               Justin Trudeau ()

               Jagmeet Singh ()

               Elizabeth May ()

          Yves-François Blanchet ()




End of Block: CSES parties and leaders - Phone-to-web wording - Leaders



                                                                                                  351
Start of Block: CSES Left - right scales



pes19_lr_parties In politics people sometimes talk of left and right. On a scale from 0 to 10
where 0 means the left and 10 means the right, where would you place each party?

If you do not know, or prefer not to answer, please click →
                                                        Left               Right           Don't know /
                                                                                           Prefer not to
                                                                                             answer

                                                   0   1       2   3   4    5      6   7     8    9   10

         Federal Conservative Party ()

            Federal Liberal Party ()

    Federal New Democratic Party (NDP) ()

            Federal Green Party ()

               Bloc Québécois ()




pes19_lr_parties En politique, on parle parfois de gauche et de droite. Où placeriez-vous ces
partis sur une échelle de 0 à 10 où 0 signifie la gauche et 10 la droite?

Si vous ne le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →
                                                   Gauche            Droite       Ne Sais pas/
                                                                                 Préfère ne pas
                                                                                    répondre

                                                   0   1       2   3   4    5      6   7     8    9   10




                                                                                                      352
      Parti conservateur du Canada ()

         Parti libéral du Canada ()

    Nouveau Parti démocratique (NPD) ()

                Parti vert ()

             Bloc québécois ()




Page Break




                                          353
pes19_lr_self In politics, people sometimes talk of left and right. Where would you place yourself
on this scale?

If you do not know, or prefer not to answer, please click →
                                                        Left               Right           Don't know /
                                                                                           Prefer not to
                                                                                             answer

                                                   0   1       2   3   4    5      6   7     8    9   10

                    &nbsp ()




pes19_lr_self En politique, on parle parfois de gauche et de droite. Où vous placeriez-vous sur
cette échelle?

Si vous ne le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →
                                                   Gauche            Droite       Ne sais pas/
                                                                                 Préfère ne pas
                                                                                    répondre

                                                   0   1       2   3   4    5      6   7     8    9   10

                    &nbsp ()




End of Block: CSES Left - right scales



   9.3.27      Module questions

NOTE: There were two large sets of questions, of which the respondent
would receive one: either the Comparative Study of Electoral Systems
(CSES) Module 5 questions, or the questions related to other projects.
The two sets of questions were designed to take roughly the same
amount of time for respondents to complete.

   4.1.1.4     EMB questions


Start of Block: EMB - statements



                                                                                                      354
pes19_likert_int_emb How much do you agree or disagree with the following statements?

pes19_likert_int_emb À quel point êtes-vous en accord ou en désaccord avec l’affirmation
suivante? Cliquez → pour voir le premier énoncé.



Page Break



pes19_emb_none Election ballots should have the option 'None of the above' for those who do
not support any of the candidates.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_emb_none Les bulletins de vote devraient inclure l'option "Aucun de ces candidats" pour
ceux et celles qui n'appuient aucun des candidats.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)

                                                                                           355
Page Break



pes19_emb_id Canadian electors should be issued a national identification card to help them
prove their identity and address when voting in federal elections.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_emb_id Les électeurs canadiens devraient recevoir une carte d'identité nationale les
aidant à prouver leur identité et leur adresse lorsqu'ils votent aux élections fédérales.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
Page Break




                                                                                             356
pes19_emb_vote16 The voting age for voting in a federal election should be lowered from 18 to
16 years old.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_emb_vote16 L'âge d'éligibilité pour voter aux élections fédérales devrait passer de 18 à
16 ans.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
Page Break




                                                                                           357
pes19_lowturnout Low voter turnout weakens Canadian democracy.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_lowturnout Le faible taux de participation affaiblit la démocratie canadienne.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
Page Break




                                                                                       358
pes19_internetvote1 How much do you agree or disagree with the following statement?

Canadians should have the option to vote over the Internet in federal elections.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_internetvote1 Les Canadiens devraient pouvoir voter par Internet lors des élections
fédérales.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
Page Break




                                                                                            359
pes19_internetvote2 If you could vote over the internet, how likely would you be to do so?

   o Very likely (1)
   o Somewhat likely (2)
   o Not very likely (3)
   o Not at all likely (4)
   o Don't know/ Prefer not to answer (5)
pes19_internetvote2 Si vous pouviez voter sur Internet, quelle serait la probabilité que vous le
fassiez?

   o Très probable (1)
   o Assez probable (2)
   o Peu probable (3)
   o Improbable (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
End of Block: EMB - statements

Start of Block: EMB - Democratic Checkup: confidence and federal satisfaction




                                                                                              360
pes19_conf_inst1 Please indicate how much confidence you have in the following:
                                                                               Don't know/
                    A great deal   Quite a lot    Not very       None at all
                                                                               Prefer not to
                        (1)           (2)         much (3)          (4)
                                                                                answer (5)
  The federal
  government
      (5)                o              o             o               o              o
      Your
  provincial or
    territorial
  government             o              o             o               o              o
        (6)

  The media
     (7)                 o              o             o               o              o
pes19_conf_inst1 Quelle confiance accordez-vous aux institutions suivantes:
                                                                                Je ne sais
                                                                Pas du tout    pas/ Préfère
                    Beaucoup (1)    Assez (2)      Peu (3)
                                                                    (4)           ne pas
                                                                               répondre (5)
       Le
 gouvernement
   fédéral (5)            o              o             o              o              o
      Votre
 gouvernement
  provincial ou
  territorial (6)
                          o              o             o              o              o
  Les médias
      (7)                 o              o             o              o              o

Page Break




                                                                                         361
pes19_conf_inst2 Please indicate how much confidence you have in the following:
                                                                              Don't know/
                 A great deal    Quite a lot     Not very       None at all
                                                                              Prefer not to
                     (1)            (2)          much (3)          (4)
                                                                               answer (5)

  The courts
     (8)               o              o              o               o              o
  Organized
  religion (9)         o              o              o               o              o
  The armed
  forces (10)          o              o              o               o              o
    Public
 schools (11)          o              o              o               o              o
 Big business
     (12)              o              o              o               o              o
    Labour
  unions (13)          o              o              o               o              o
   The public
  service (14)         o              o              o               o              o
  The police
    (15)               o              o              o               o              o
  Elections
 Canada (16)           o              o              o               o              o




                                                                                        362
pes19_conf_inst2 Quelle confiance accordez-vous aux institutions suivantes:
                                                                               Je ne sais
                                                                Pas du tout   pas/ Préfère
                  Beaucoup (1)    Assez (2)        Peu (3)
                                                                    (4)          ne pas
                                                                              répondre (5)

 Les tribunaux
       (8)             o               o              o               o             o
  La religion
 organisée (9)         o               o              o               o             o
  Les forces
 armées (10)           o               o              o               o             o
  Les écoles
  publiques
     (11)              o               o              o               o             o
 Les grandes
  entreprises
      (12)             o               o              o               o             o
 Les syndicats
     (13)              o               o              o               o             o
  Le service
 publique (14)         o               o              o               o             o
 La police (15)
                       o               o              o               o             o
  Élections
 Canada (16)           o               o              o               o             o

Page Break




                                                                                        363
NOTE: ${e://Field/confidence_institutions_word} ) was randomly set to
be either “confident” in English (“confiant” in French) or “worried”
(“inquiet” in French).

pes19_foreign How ${e://Field/confidence_institutions_word} are you that our elections are safe
from foreign interference?

   o Very ${e://Field/confidence_institutions_word} (1)
   o Somewhat ${e://Field/confidence_institutions_word} (2)
   o Not very ${e://Field/confidence_institutions_word} (3)
   o Not at all ${e://Field/confidence_institutions_word} (4)
   o Don't know/ Prefer not to answer (5)
pes19_foreign À quel point êtes-vous ${e://Field/confidence_institutions_word_fr} que nos
élections sont à l'abri de l'interférence étrangère?

   o Très ${e://Field/confidence_institutions_word_fr} (1)
   o Assez ${e://Field/confidence_institutions_word_fr} (2)
   o Pas très ${e://Field/confidence_institutions_word_fr} (3)
   o Pas du tout ${e://Field/confidence_institutions_word_fr} (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
Page Break




                                                                                            364
pes19_emb_satif How satisfied are you with the way Elections Canada runs federal elections?

   o Very satisfied (1)
   o Fairly satisfied (2)
   o Not very satisfied (3)
   o Not satisfied at all (4)
   o Don't know/ Prefer not to answer (5)
pes19_emb_satif À quel point êtes-vous satisfait de la façon dont Élections Canada a pris en
charge les élections fédérales?

   o Très satisfait (1)
   o Assez satisfait (2)
   o Pas très satisfait (3)
   o Pas du tout satisfait (4)
   o Je ne sais pas/ Préfère ne pas répondre (5)
Page Break




                                                                                           365
pes19_emb8 Thinking about this election, would you say that Elections Canada ran the
election…

   o Very fairly (1)
   o Somewhat fairly (2)
   o Not very fairly (3)
   o Not at all fairly (4)
   o Don't know/ Prefer not to answer (5)
pes19_emb8 En pensant à la dernière élection, croyez-vous qu'Élections Canada a conduit
l'élection…

   o De façon très juste (1)
   o De façon assez juste (2)
   o Pas très justement (3)
   o Pas justement du tout (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
End of Block: EMB - Democratic Checkup: confidence and federal satisfaction

Start of Block: EMB - Internet voting




                                                                                          366
pes19_internetregis To complete voter registration online, electors must provide their date of
birth, home address, and driver’s license number on Elections Canada’s website. How
comfortable are you with providing this information online to Elections Canada?

   o Very comfortable (1)
   o Somewhat comfortable (2)
   o Not very comfortable (3)
   o Not at all comfortable (4)
   o Don't know/ Prefer not to answer (5)
pes19_internetregis
Pour compléter leur enregistrement en ligne, les électeurs devraient fournir leur date de
naissance, leur adresse et leur numéro de permis de conduire sur le site d'Élections Canada.
À quel point seriez vous à l'aise de fournir ces informations en ligne à Élections Canada?

   o Très à l'aise (1)
   o Un peu à l'aise (2)
   o Pas très à l'aise (3)
   o Pas du tout à l'aise (4)
   o Ne sais pas / Préfère ne pas répondre (5)
Page Break




                                                                                                 367
pes19_internetrisk1 Which statement comes closest to your own view?

   o Voting on the Internet is risky. (1)
   o Voting on the Internet is safe. (2)
   o Don't know/ Prefer not to answer (3)
pes19_internetrisk1 Quelle affirmation reflète le mieux votre opinion?

   o Voter sur Internet est risqué (1)
   o Voter sur Internet est sécuritaire (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)
Page Break




                                                                         368
pes19_internetrisk2 Which statement comes closest to your own view?

   o Registering to vote on the Internet is risky. (1)
   o Registering to vote on the Internet is safe. (2)
   o Don't know/ Prefer not to answer (3)
pes19_internetrisk2 Quelle affirmation reflète le mieux votre opinion?

   o S'enregistrer sur Internet pour voter est risqué (1)
   o S'enregistrer sur Internet pour voter est sécuritaire (2)
   o Je ne sais pas / Préfère ne pas répondre (3)
End of Block: EMB - Internet voting



   4.1.1.5      Elections Ontario questions


Start of Block: Elections Ontario 1
Display This Question:
    If Are you a... = Canadian citizen


pes19_emb_register Did you receive a voter registration card in the mail?

   o Yes (1)
   o No (2)
   o Don't know (3)
   o Prefer not to answer (4)



                                                                            369
pes19_emb_register Avez-vous reçu une carte d'information de l'électeur par la poste?

   o Oui (1)
   o Non (2)
   o Je ne sais pas (3)
   o Préfère ne pas répondre (4)
Page Break




                                                                                        370
Display This Question:
    If Did you receive a voter registration card in the mail? = Yes


pes19_emb_card Was the information on your voter registration card correct?

   o Yes (1)
   o No (2)
   o Don't know/ Prefer not to answer (3)
pes19_emb_card Les informations sur votre carte d'information de l'électeur étaient-elles
correctes?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)
Page Break




                                                                                            371
Display This Question:
    If Are you a... = Canadian citizen
    And Did you receive a voter registration card in the mail? = No


pes19_emb_register2 Did you register to vote during the election?

   o Yes (1)
   o No (2)
   o Don't know/ Prefer not to answer (3)
pes19_emb_register2 Vous êtes-vous enregistré lors de l'élection pour pouvoir voter?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)
Page Break




                                                                                       372
Display This Question:
    If Did you register to vote during the election? = Yes


pes19_emb_reg_how How did you register to vote?

   o Online through the Elections Canada website (1)
   o At my local Elections Canada office (2)
   o At the polls (3)
   o By mail (4)
   o Don't know/ Prefer not to answer (5)
pes19_emb_reg_how Comment aves-vous vous enregistré lors de l'élection pour pouvoir voter?

   o En ligne sur le site d'Élections Canada (1)
   o À un bureau local d'Élections Canada (2)
   o Aux urnes (3)
   o Par la poste (4)
   o Je ne sais pas/ Préfère ne pas répondre (5)
Page Break




                                                                                      373
Display This Question:
    If Did you register to vote during the election? = Yes


pes19_emb_register3 How easy or difficult did you find it to register to vote?

   o Very easy (1)
   o Somewhat easy (2)
   o Neither easy nor difficult (3)
   o Somewhat difficult (4)
   o Very difficult (5)
   o Don't know/ Prefer not to answer (6)
pes19_emb_register3 À quel point a-t-il été facile de vous enregistrer pour voter?

   o Très facile (1)
   o Plutôt facile (2)
   o Ni facile, ni difficile (3)
   o Plutôt difficile (4)
   o Très difficile (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
Page Break




                                                                                     374
Display This Question:
    If Are you a... = Canadian citizen




                                         375
pes19_emb4 From which of the following sources did you get information about voting in the
federal election? (Select all that apply)


   ▢          Elections Canada flyer (1)


   ▢          Voter Information Card (2)


   ▢          Advertisements from Elections Canada (3)


   ▢          Radio or Television (4)


   ▢          Newspaper (5)


   ▢          Elections Canada website (6)


   ▢          Word of mouth (7)


   ▢          Facebook (8)


   ▢          Twitter (9)


   ▢          YouTube (10)


   ▢        Other social media (11)
   ________________________________________________


   ▢          From internet website other than Elections Canada (12)


   ▢          From candidates or political parties (13)


   ▢          Other source (14) ________________________________________________




                                                                                             376
▢   ⊗None of these (15)

▢   ⊗Don't know/ Prefer not to answer (16)




                                             377
pes19_emb4 De quelles sources avez-vous reçu des informations sur le vote aux élections
fédérales? (Séléctionnez toutes les sources qui s'appliquent)


   ▢          Bulletin d'Élections Canada (1)


   ▢          Carte d'information de l'électeur (2)


   ▢          Publicités d'Élections Canada (3)


   ▢          Radio ou télévision (4)


   ▢          Journal (5)


   ▢          Site d'Élections Canada (6)


   ▢          Bouche à oreille (7)


   ▢          Facebook (8)


   ▢          Twitter (9)


   ▢          YouTube (10)


   ▢        Autres médias sociaux (11)
   ________________________________________________


   ▢          À partir d'un site Web autre qu'Élections Canada (12)


   ▢          Des candidats ou des partis politiques (13)


   ▢          Autre source (14) ________________________________________________




                                                                                          378
   ▢           ⊗Aucun (15)

   ▢           ⊗Je ne sais pas/ Préfère ne pas répondre (16)
End of Block: Elections Ontario 1

Start of Block: Elections Ontario 2



pes19_emb7 Thinking about the recent election, how informed did you feel about the following
elements of the voting process?


If you do not know, or prefer not to answer, please click →
                                                    Not informed at all           Very informed

                                                  0    1   2    3   4     5   6     7   8   9     10

 What documentation was required to vote ()

                Where to vote ()

  How to vote at an advance polling station ()




pes19_emb7
En ce qui concerne les dernières élections, nous aimerions savoir à quel point vous vous
sentiez informé au sujet des différents éléments du processus électoral ci-dessous:


Si vous ne savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →
                                                 Pas du tout informé          Très informé

                                                  0    1   2    3   4     5   6     7   8   9     10




                                                                                                  379
  Quelle documentation était nécessaire pour
                  voter ()
                   Où voter ()

     Comment voter les jours de vote par
              anticipation ()




Page Break



pes19_emb_info How easy or difficult was it to find the information you needed to vote?

   o Extremely easy (1)
   o Somewhat easy (2)
   o Neither easy nor difficult (3)
   o Somewhat difficult (4)
   o Extremely difficult (5)
   o Don't know/ Prefer not to answer (6)
pes19_emb_info À quel point était-il facile ou difficile de trouver les informations dont vous aviez
besoin pour voter?

   o Très facile (1)
   o Plutôt facile (2)
   o Ni facile, ni difficile (3)
   o Plutôt difficile (4)
   o Très difficile (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
                                                                                                380
End of Block: Elections Ontario 2



   4.1.1.6    Provincial election


Start of Block: Other: Provincial election




                                             381
pes19_provvote If a provincial election were held today in
${pes19_province/ChoiceGroup/SelectedChoices}, which party would you vote for?
In which province or territory are you currently living? != Saskatchewan

    o Liberal (281)
In which province or territory are you currently living? != Quebec
And In which province or territory are you currently living? != Prince Edward Island

    o NDP (282)
In which province or territory are you currently living? = British Columbia
Or In which province or territory are you currently living? = Ontario
Or In which province or territory are you currently living? = New Brunswick
Or In which province or territory are you currently living? = Prince Edward Island

    o Green (283)
In which province or territory are you currently living? = Quebec

    o Coalition Avenir Québec (284)
In which province or territory are you currently living? = Quebec

    o Parti Québécois (285)
In which province or territory are you currently living? = Quebec

    o Québec Solidaire (286)
In which province or territory are you currently living? = Alberta

    o United Conservative (288)
In which province or territory are you currently living? = Alberta

    o Alberta Party (289)
In which province or territory are you currently living? = Alberta

    o Conservative (290)
In which province or territory are you currently living? = Saskatchewan

    o Saskatchewan Party (291)
In which province or territory are you currently living? = Nova Scotia
Or In which province or territory are you currently living? = Newfoundland and Labrador



                                                                                          382
Or In which province or territory are you currently living? = New Brunswick
Or In which province or territory are you currently living? = Prince Edward Island
Or In which province or territory are you currently living? = Ontario
Or In which province or territory are you currently living? = Manitoba

    o Progressive Conservative (292)
In which province or territory are you currently living? = New Brunswick

    o People's Alliance (298)
In which province or territory are you currently living? = Yukon

    o Yukon Party (293)
    o Another party (please specify) (295)
    ________________________________________________

    o None of these (296)
    o Don't know/ Prefer not to answer (297)




                                                                                     383
pes19_provvote En politique provinciale, vous considérez-vous habituellement comme étant:
In which province or territory are you currently living? != Saskatchewan

    o Parti libéral (281)
In which province or territory are you currently living? != Quebec
And In which province or territory are you currently living? != Prince Edward Island

    o NPD (282)
In which province or territory are you currently living? = British Columbia
Or In which province or territory are you currently living? = Ontario
Or In which province or territory are you currently living? = New Brunswick
Or In which province or territory are you currently living? = Prince Edward Island

    o Parti vert (283)
In which province or territory are you currently living? = Quebec

    o Coalition avenir Québec (284)
In which province or territory are you currently living? = Quebec

    o Parti québécois (285)
In which province or territory are you currently living? = Quebec

    o Québec solidaire (286)
In which province or territory are you currently living? = Alberta

    o United Conservative (288)
In which province or territory are you currently living? = Alberta

    o Alberta Party (289)
In which province or territory are you currently living? = Alberta

    o Parti conservateur (290)
In which province or territory are you currently living? = Saskatchewan

    o Saskatchewan Party (291)
In which province or territory are you currently living? = Nova Scotia
Or In which province or territory are you currently living? = Newfoundland and Labrador
Or In which province or territory are you currently living? = New Brunswick



                                                                                          384
Or In which province or territory are you currently living? = Prince Edward Island
Or In which province or territory are you currently living? = Ontario
Or In which province or territory are you currently living? = Manitoba

    o Parti progressiste-conservateur du Canada (292)
In which province or territory are you currently living? = New Brunswick

    o Alliance des gens du Nouveau-Brunswick (298)
In which province or territory are you currently living? = Yukon

    o Yukon Party (293)
    o Autre parti (veuillez spécifier) (295)
    ________________________________________________

    o Aucun de ces partis (296)
    o Je ne sais pas/Préfère ne pas répondre (297)
End of Block: Other: Provincial election



    9.3.28       Interest in politics


Start of Block: Interest in politics

pes19_interest How interested are you in politics generally? Use a scale from 0 to 10, where
zero means no interest at all, and ten means a great deal of interest.


If you do not know, or prefer not to answer, please click →
                                                  No interest at A great deal of             Don't know /
                                                        all         interest                 Prefer not to
                                                                                               answer

                                                        0    1     2     3   4   5   6   7     8    9   10

                      &nbsp ()




                                                                                                        385
pes19_interest

                         Quel est votre intérêt pour la politique en général? Veuillez répondre
entre 0 et 10, où 0 signifie aucun intérêt du tout et 10 signifie beaucoup d’intérêt. Si vous ne
le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →

                                                Pas d'intérêt du    Beaucoup       Ne sais pas/
                                                     tout            d'intérêt    Préfère ne pas
                                                                                     répondre

                                                  0   1    2   3    4   5    6   7    8   9   10

                   &nbsp ()




End of Block: Interest in politics



   9.3.29      Social networks


Start of Block: Democracy Checkup: social network


pes19_socnet1 Thinking about people who are NOT family members or relatives, how many
close friends do you have?

   o None (1)
   o 1 (2)
   o 2-5 (3)
   o More than 5 (4)
   o Don't know/ Prefer not to answer (5)




                                                                                              386
pes19_socnet1 En considérant uniquement les gens qui ne font PAS partie de votre famille
immédiate ou élargie, combien d'amis proches avez-vous?

   o Aucun (1)
   o 1 (2)
   o 2-5 (3)
   o Plus de 5 (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
Display This Question:
    If Thinking about people who are NOT family members or relatives, how many close friends do you
have? != None
    And Thinking about people who are NOT family members or relatives, how many close friends do
you have? != Don't know/ Prefer not to answer


pes10_socnet3 In an average month, how often do you get together in person with your close
friends?

   o Daily (1)
   o More than once a week (2)
   o Weekly (3)
   o More than once a month (4)
   o Once a month (5)
   o Less than once a month (6)
   o Don't know/ Prefer not to answer (7)



                                                                                                 387
pes10_socnet3 Lors d'un mois typique, à quelle fréquence rencontrez-vous vos amis proches
en personne?

   o Quotidiennement (1)
   o Plus d'une fois par semaine (2)
   o À chaque semaine (3)
   o Plus d'une fois par mosi (4)
   o Une fois par mois (5)
   o Moins d'une fois par mois (6)
   o Je ne sais pas / Préfère ne pas répondre (7)
Page Break




                                                                                        388
Display This Question:
    If Thinking about people who are NOT family members or relatives, how many close friends do you
have? != None
    And Thinking about people who are NOT family members or relatives, how many close friends do
you have? != Don't know/ Prefer not to answer




pes19_socnet2 How many of your close friends …
                                                   Thinking about
                                                     people who
                                                       are NOT
                                                        family
                                                     members or      Thinking about
                                                   relatives, how      people who
                                                     many close          are NOT
                                                   friends do you         family
                                                    have? = 2-5        members or
                                                                     relatives, how
                                                                                      Don't know/
                     None (1)          1 (2)          Or Thinking                     Prefer not to
                                                     about people      many close
                                                                     friends do you    answer (5)
                                                     who are NOT
                                                         family      have? = More
                                                      members or          than 5
                                                    relatives, how   More than 5
                                                      many close         (4)
                                                    friends do you
                                                    have? = More
                                                         than 5
                                                       2-5 (3)
  Belong to a
     visibly
    different
 ethnicity than          o                o                o                o               o
   you? (1)
    Tend to
 disagree with
   you about
  politics? (2)
                         o                o                o                o               o
    Have a
  graduate or
  professional
  degree? (3)
                         o                o                o                o               o



                                                                                                 389
pes19_socnet2 Parmi vos amis proches, combien d'entre eux...
                                                    Thinking
                                                 about people
                                                 who are NOT
                                                     family
                                                  members or
                                                relatives, how       Thinking
                                                  many close      about people
                                                friends do you    who are NOT
                                                 have? = 2-5          family       Je ne sais
                                                                   members or
                                                  Or Thinking    relatives, how
                                                                                  pas / Préfère
                     Aucun (1)       1 (2)
                                                 about people      many close        ne pas
                                                 who are NOT     friends do you   répondre (5)
                                                     family          have? =
                                                  members or       More than 5
                                                relatives, how
                                                  many close     Plus de 5 (4)
                                                friends do you
                                                    have? =
                                                  More than 5
                                                   2-5 (3)
 Appartiennent à
  une ethnicité
   visiblement
 différente de la         o            o              o                o                o
    vôtre? (1)
  Tendent à être
  en désaccord
   avec vous au
    sujet de la           o            o              o                o                o
   politique? (2)
   Possèdent un
 diplôme d'études
  supérieures ou
 professionnelles?        o            o              o                o                o
        (3)




Page Break




                                                                                            390
End of Block: Democracy Checkup: social network

Start of Block: Discussion of politics with Social Networks


pes19_discfam How often do you discuss politics with family and friends?

   o Never (1)
   o Sometimes (2)
   o Often (3)
   o All the time (4)
   o Don't know/ Prefer not to answer (5)
pes19_discfam À quelle fréquence discutez-vous de politique avec votre famille et vos amis?

   o Jamais (1)
   o Parfois (2)
   o Souvent (3)
   o Tout le temps (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
Page Break




                                                                                          391
pes19_discwork How often do you discuss politics with people at your work or school?

   o Never (1)
   o Sometimes (2)
   o Often (3)
   o All the time (4)
   o Don't know/ Prefer not to answer (5)
pes19_discwork À quelle fréquence discutez-vous de politique avec des gens au travail ou à
l’école?

   o Jamais (1)
   o Parfois (2)
   o Souvent (3)
   o Tout le temps (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
Page Break




                                                                                             392
pes19_disagreed During the last month, how often have you discussed politics with someone
who disagreed with your political views?

   o Never (1)
   o Sometimes (2)
   o Often (3)
   o All the time (4)
   o Don't know/ Prefer not to answer (5)
pes19_disagreed                Au cours du dernier mois, à quelle fréquence avez-vous discuté
de politique avec quelqu’un qui n’était pas d’accord avec vos opinions politiques?

   o Jamais (1)
   o Quelques fois (2)
   o Souvent (3)
   o Tout le temps (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
End of Block: Discussion of politics with Social Networks



   9.3.30     Participation


NOTE: The order of the three participation questions was randomized.


Start of Block: Democracy Checkup: participation - protest




                                                                                          393
pes19_partic1 Here are some things people can do to participate in politics. Please indicate how
many times you've done these things over the past 12 months.
                                                                                   Don't know/
                                                 A few times       More than
                   Never (1)     Just once (2)                                    Prefer not to
                                                     (3)         five times (4)
                                                                                   answer (5)
   Attended a
    political
   meeting or
   speech (7)
                         o              o               o               o               o
  Attended a
     rally or
 participated in
  a protest or
 demonstration
                         o              o               o               o               o
       (8)
  Boycotted or
     bought
  products for
    ethical,
 environmental,          o              o               o               o               o
   or political
  reasons (9)




                                                                                            394
pes19_partic1 Voici certaines choses que les gens peuvent faire pour participer à la vie
politique. Veuillez indiquer combien de fois vous avez fait ces choses au cours des 12 derniers
mois.
                                                                                     Je ne sais
                                      Juste une       Quelques        Plus de       pas / Préfère
                       Jamais (1)
                                       fois (2)        fois (3)     cinq fois (4)      ne pas
                                                                                    répondre (5)
   Participé à une
    réunion ou un
  discours politique
          (7)
                             o             o              o               o               o
   Participé à une
    marche, un
 rassemblement ou
 une manifestation           o             o              o               o               o
          (8)
     Acheté des
  produits pour des
  raisons politique,
     éthiques ou
 environnementales
                             o             o              o               o               o
          (9)



End of Block: Democracy Checkup: participation - protest

Start of Block: Democracy Checkup: participation - institution




                                                                                              395
pes19_partic2 Here are some things people can do to participate in politics. Please indicate how
many times you've done these things over the past 12 months.
                                                                                   Don't know/
                                                  A few times      More than
                    Never (1)    Just once (2)                                    Prefer not to
                                                      (3)        five times (4)
                                                                                   answer (5)
  Followed any
 elected officials
  or candidates
   for office on
  social media
                         o               o              o               o               o
        (1)
 Volunteered for
 a political party
  or candidate
        (2)
                         o               o              o               o               o
   Contacted an
      elected
  representative
     (federal,
   provincial or         o               o              o               o               o
 local/municipal)
        (3)
    Donated
   money to a
    political
  candidate or           o               o              o               o               o
    party (4)




                                                                                            396
pes19_partic2 Voici certaines choses que les gens peuvent faire pour participer à la vie
politique. Veuillez indiquer combien de fois vous avez fait ces choses au cours des 12 derniers
mois.
                                                                                   Je ne sais
                                    Juste une       Quelques      Plus de cinq    pas / Préfère
                    Jamais (1)
                                     fois (2)        fois (3)        fois (4)        ne pas
                                                                                  répondre (5)
 Suivi un élu ou
  un candidate
 sur les médias
   sociaux (1)
                         o               o               o              o               o
     Fait du
 bénévolat pour
 un parti ou un
    candidat             o               o               o              o               o
  politique (2)
   Contacté un
   représentant
     politique
     (fédéral,
   provincial ou         o               o               o              o               o
 local/municipal)
        (3)
   Fait un don
   auprès d'un
   candidat ou
  parti politique        o               o               o              o               o
        (4)



End of Block: Democracy Checkup: participation - institution

Start of Block: Democracy Checkup: participation - civic




                                                                                            397
pes19_partic3 Here are some things people can do to participate in politics. Please indicate how
many times you've done these things over the past 12 months.




                                                                                            398
                                                                            Don't know/
                                             A few times     More than
                 Never (1)   Just once (2)                                  Prefer not to
                                                 (3)       five times (4)
                                                                             answer (5)
 Volunteered
for a group or
 organization
like a school,
  a religious
organization,
  or sports or
                     o             o              o              o                o
  community
 associations
      (25)
  Donated
 money to a
 charitable
 cause (26)
                     o             o              o              o                o
Been active
 in another
   group or
organization
  (e.g. local
organization,
church, arts         o             o              o              o                o
   or hobby
    group,
   women’s
 group) (27)
  Circulated,
(re)posted or
 commented
  on political
 information,
   news or           o             o              o              o                o
    content
   online or
  offline (29)
Used social
  media to
  discuss
 politics or
  political
                     o             o              o              o                o
issues (30)




                                                                                      399
 Signed a
petition in
person or
online (31)
              o   o   o   o   o




                                  400
pes19_partic3 Voici certaines choses que les gens peuvent faire pour participer à la vie
politique. Veuillez indiquer combien de fois vous avez fait ces choses au cours des 12 derniers
mois .




                                                                                            401
                                                                        Je ne sais
                                Juste une   Quelques    Plus de cinq   pas / Préfère
                   Jamais (1)
                                 fois (2)    fois (3)      fois (4)       ne pas
                                                                       répondre (5)
     Fait du
bénévolat pour
       une
 organisation,
  par exemple
une école, une
  organisation
 religieuse, ou        o            o           o            o               o
       une
  association
   sportive ou
communautaire
       (25)
Fait un don à
 une oeuvre
caritative (26)        o            o           o            o               o
 Été actif dans
     un autre
groupe ou une
       autre
  organisation
 (par exemple,
        une
  organisation
   locale, une         o            o           o            o               o
    église, un
      groupe
artistique ou de
     loisir, un
    groupe de
 femmes) (27)
  Fait circuler,
   partagé ou
commenté de
 l'information,
des nouvelles
ou du contenu          o            o           o            o               o
  politique en
 ligne ou hors
    ligne (29)




                                                                                 402
    Utilisé les
 médias sociaux
 afin de discuter
 de politique ou
     d'enjeux
                        o              o              o         o   o
 politiques (30)
   Signé une
   pétition en
  ligne ou en
 personne (31)
                        o              o              o         o   o

End of Block: Democracy Checkup: participation - civic


   9.3.31     Voluntary associations


NOTE: pes19_volassoc was set to receive a split sample of 50% (1/2),
to make room in the survey for more questions. Whether a respondent
was assigned to receive pes19_volassoc was randomly determined in the
Survey Flow by setting the embedded data field split_vol_assoc to
either 0 or 1. If split_vol_assoc was equal to 1, they were assigned
to receive pes19_volassoc. split_vol_assoc can be used to filter the
dataset to only respondents that were assigned to receive
pes19_volassoc.


Start of Block: Participation battery: Voluntary associations




                                                                        403
pes19_volassoc Please indicate whether you have been active in any of the following voluntary
associations during the past five years. Select all that apply.


   ▢          Community service group (1)


   ▢          Business association (2)


   ▢          Professional association (3)


   ▢          Environmental group (4)


   ▢          Women's group (5)


   ▢          Labour union (6)


   ▢          Ethnic association (7)


   ▢          Sports association (8)


   ▢          Religious organization (9)


   ▢          Parents' group (10)


   ▢          Farmers' association (11)


   ▢        Other (please specify) (12)
   ________________________________________________


   ▢          ⊗Not active in any of these associations (13)

   ▢          ⊗Don't know/ Prefer not to answer (14)


                                                                                          404
pes19_volassoc Veuillez indiquer si vous avez été actif dans l’une des associations bénévoles
suivantes au cours des CINQ dernières années. Veuillez sélectionner toutes les réponses qui
s'appliquent.


   ▢          Groupe de service communautaire (1)


   ▢          Association commerciale (2)


   ▢          Association professionnelle (3)


   ▢          Groupe environnemental (4)


   ▢          Groupe de femmes (5)


   ▢          Syndicat (6)


   ▢          Association ethnique (7)


   ▢          Association sportive (8)


   ▢          Organisation religieuse (9)


   ▢          Groupes de parents (10)


   ▢          Association de fermiers (11)


   ▢        Autre (spécifiez svp) (12)
   ________________________________________________


   ▢          ⊗Je n’ai pas été actif au sein de ces associations (13)

   ▢          ⊗Je ne sais pas/ Préfère ne pas répondre (14)

                                                                                           405
End of Block: Participation battery: Voluntary associations

   9.3.32     Party membership in lifetime


Start of Block: Party Member - Lifetime


pes19_partymember Have you ever been a member of a provincial or federal political party?

   o Yes (1)
   o No (2)
   o Don't know/Prefer not to answer (3)
pes19_partymember Avez-vous déjà été membre d'un parti politique provincial ou fédéral?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)
End of Block: Party Member - Lifetime



   9.3.33     Importance of voting


Start of Block: Importance of voting


pes19_diff_power Some people say that it doesn't make any difference who is in power. Others
say that it makes a big difference who is in power. Using a scale where one means that it
doesn't make any difference who is in power and five means that it makes a big difference who
is in power, where would you place yourself?

If you do not know, or prefer not to answer, please click →
                                                 It doesn't make It makes a big   Don't know /
                                                  any difference    difference    Prefer not to
                                                                                    answer




                                                                                             406
                                                    1         2         3        4         5

                   &nbsp ()




pes19_diff_power Certaines personnes disent que peu importe qui est au pouvoir, ça ne fait pas
de différence. D'autres disent que la personne au pouvoir peut faire une grande différence. En
utilisant l’échelle suivante, où un signifie que la personne au pouvoir ne fait aucune différence
et que cinq signifie que la personne au pouvoir fait une grande différence, où vous situez-vous?

Si vous ne savez pas, ou préférez ne pas répondre, veuillez sélectionner →
                                               Cela ne fait     Cela fait une Je ne sais pas /
                                                 aucune             grande    Préfère ne pas
                                                différence        différence     répondre

                                                    1         2         3        4         5

                   &nbsp ()




Page Break




                                                                                               407
pes19_diff_happens Some people say that no matter who people vote for, it won't make any
difference to what happens. Others say that who people vote for can make a big difference to
what happens. Using a scale where one means that voting won't make any difference to what
happens and five means that voting can make a big difference, where would you place
yourself?

If you do not know, or prefer not to answer, please click →
                                                  Voting won't       Voting can      Don't know /
                                                   make any          make a big      Prefer not to
                                                   difference        difference        answer

                                                      1         2         3          4         5

                    &nbsp ()




pes19_diff_happens Certaines personnes disent que la personne pour qui l’on vote importe
peu, car cela n’aura aucun impact sur ce qui va se passer. D’autres estiment que le candidat
pour qui l’on vote peut faire une grande différence. En utilisant l'échelle suivante, où un signifie
que voter ne fera pas de différence et cinq, que voter peut faire une grande différence, où vous
situez-vous?

Si vous ne savez pas, ou préférez ne pas répondre, veuillez sélectionner →
                                               Voter ne fait Voter peut faire Je ne sais pas /
                                                 aucune          une grande Préfère ne pas
                                                différence        différence     répondre

                                                      1         2         3          4         5

                    &nbsp ()




End of Block: Importance of voting

Start of Block: Likert section 2 intro

pes19_likert_intro2 How much do you agree or disagree with the following statements? Please
click → to see first statement.




                                                                                                   408
pes19_likert_intro2 À quel point êtes-vous en accord ou en désaccord avec les énoncés
suivants? Cliquez → pour voir le premier énoncé.


End of Block: Likert section 2 intro



   9.3.34     Media statments


NOTE: The order of the four media questions, pes19_mediaelite,
pes19_medianolie, pes19_opinion and pes19_lookslikeme, was randomized


Start of Block: Media 1


pes19_mediaelite Mainstream news media is largely controlled by elite interests.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                        409
pes19_mediaelite Les médias grand public sont largement contrôlés par des intérêts extérieurs
élitistes.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Media 1

Start of Block: Media 2


pes19_medianolie Journalists who work for mainstream news media never lie.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                          410
pes19_medianolie Les journalistes qui travaillent pour les médias grand public ne mentent
jamais.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Media 2

Start of Block: Media 3


pes19_opinion Even opinions that are not based on fact should be given consideration in public
life.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                            411
pes19_opinion Même les opinions qui ne sont pas appuyées sur des faits devraient être
considérées dans l'espace public.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Media 3

Start of Block: Media 4


pes19_lookslikeme I feel that I am better represented by someone who looks like me.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                        412
pes19_lookslikeme Je sens que je suis mieux représenté(e) par quelqu'un qui me ressemble.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Media 4



   9.3.35     Representation by women


Start of Block: Statement: Protect women


pes19_womenparl The best way to protect women's interests is to have more women in
Parliament.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)



                                                                                        413
pes19_womenparl Le meilleur moyen de protéger les intérêts des femmes est d'avoir plus de
femmes au Parlement…

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Statement: Protect women



   9.3.36     Corruption


Start of Block: Corruption


pes19_corruption How widespread do you think corruption such as bribe taking is among
politicians in Canada?

   o Very widespread (1)
   o Quite widespread (2)
   o Not very widespread (3)
   o It hardly happens at all (4)
   o Don't know/ Prefer not to answer (5)



                                                                                        414
pes19_corruption À quel point croyez-vous que la corruption, comme les pots-de-vin, soit un
phénomène répandu parmi les politiciens au Canada?

   o Très répandu (1)
   o Assez répandu (2)
   o Pas très répandu (3)
   o Cela n'arrive presque jamais (4)
   o Je ne sais pas/ Préfère ne pas répondre (5)
End of Block: Corruption



   9.3.37     Populism


NOTE: The order of the eight populism questions was randomized.


Start of Block: Populism battery intro


pes19_populism_intro How much do you agree or disagree with the following statements?
Please click → to see first statement.

pes19_populism_intro À quel point êtes-vous en accord ou désaccord avec les énoncés
suivants? Cliquez → pour voir le premier énoncé.


End of Block: Populism battery intro

Start of Block: Populism battery 1




                                                                                              415
pes19_populism_1 You feel you understand the most important political issues of this country.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_populism_1 J'ai l’impression de comprendre les enjeux politiques les plus importants de
ce pays.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Populism battery 1

Start of Block: Populism battery 2


pes19_populism_2




                                                                                           416
What people call compromise in politics is really just selling out on one's principles.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_populism_2 En politique, les compromis équivalent à renoncer à ses principes.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Populism battery 2

Start of Block: Populism battery 3




                                                                                          417
pes19_populism_3 Most politicians do not care about the people.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_populism_3 La plupart des politiciens ne se soucient pas du peuple.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Populism battery 3

Start of Block: Populism battery 4




                                                                            418
pes19_populism_4 Most politicians are trustworthy.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_populism_4 La plupart des politiciens sont dignes de confiance.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Populism battery 4

Start of Block: Populism battery 5




                                                                        419
pes19_populism_5 Politicians are the main problem in Canada.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_populism_5 Les politiciens sont le principal problème au Canada.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Populism battery 5

Start of Block: Populism battery 6




                                                                         420
pes19_populism_6 Having a strong leader in government is good for Canada even if the leader
bends the rules to get things done.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_populism_6           Avoir un leader fort à la tête du gouvernement est bon pour le
Canada même si ce leader contourne les règles pour faire avancer les choses.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Populism battery 6

Start of Block: Populism battery 7




                                                                                            421
pes19_populism_7 The people, and not politicians, should make our most important policy
decisions.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_populism_7 C'est le peuple, et non les politiciens, qui devrait prendre les décisions
politiques les plus importantes.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Populism battery 7

Start of Block: Populism battery 8




                                                                                              422
pes19_populism_8 Most politicians care only about the interests of the rich and powerful.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_populism_8 La plupart des politiciens se soucient uniquement des intérêts des gens
riches et puissants.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Populism battery 8



   9.3.38     Nativism


NOTE: The order of the five nativism questions was randomized.


Start of Block: Nativism battery 1




                                                                                            423
pes19_nativism1 Minorities should adapt to the customs and traditions of Canada.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_nativism1 Les minorités devraient s’adapter aux coutumes et traditions du Canada.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Nativism battery 1

Start of Block: Nativism battery 2




                                                                                          424
pes19_nativism2 The will of the majority should always prevail, even over the rights of
minorities.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_nativism2 La volonté de la majorité devrait toujours l’emporter, même aux dépens des
droits des minorités.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Nativism battery 2

Start of Block: Nativism battery 3




                                                                                          425
pes19_nativism3 Immigrants are generally good for Canada's economy.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_nativism3 Les immigrants sont généralement bénéfiques pour l'économie canadienne.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Nativism battery 3

Start of Block: Nativism battery 4




                                                                                      426
pes19_nativism4 Canada's culture is generally harmed by immigrants.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know / Prefer not to answer (6)
pes19_nativism4 La culture du Canada est généralement pénalisée par les immigrants.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Nativism battery 4

Start of Block: Nativism battery 5




                                                                                      427
pes19_nativism5 Immigrants increase crime rates in Canada.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_nativism5 Les immigrants augmentent le taux de criminalité au Canada.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Nativism battery 5



   9.3.39     Canadian identification


Start of Block: Canadian identification




                                                                              428
pes19_canid1 I have a lot in common with other Canadians

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_canid1
J'ai beaucoup en commun avec les autres Canadiens

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
Page Break




                                                           429
Display This Question:
    If Are you a... = Canadian citizen


pes19_canid2 I often think about the fact that I am Canadian.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_canid2 Je pense souvent au fait que je suis Canadien(ne).

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
Page Break




                                                                  430
Display This Question:
    If Are you a... = Canadian citizen


pes19_canid3 In general, I am glad to be Canadian

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_canid3
En général, je suis heureux d'être Canadien(ne)

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Canadian identification



   9.3.40       Social Dominance Orientation


NOTE: The order of the four SDO questions was randomized.




                                                            431
Start of Block: SDO - intro


pes19_sdointro There are many kinds of groups in the world: men and women, ethnic and
religious groups, nationalities, and political factions. How much do you agree or disagree with
the following ideas about groups in general?

pes19_sdointro
Il existe plusieurs groupes dans le monde: les hommes et les femmes, les groupes ethniques et
religieux, les nationalités, les factions politiques. À quel point êtes-vous en accord ou en
désaccord avec les affirmations suivantes au sujet des groupes en général?


End of Block: SDO - intro

Start of Block: SDO - 1


pes19_sdo1 If certain groups stayed in their place, we would have fewer problems.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                              432
pes19_sdo1 Si certains groupes restaient à leur place, nous aurions moins de problèmes.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: SDO - 1

Start of Block: SDO - 2


pes19_sdo2 We should do what we can to equalize conditions for different groups.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                          433
pes19_sdo2 Nous devrions faire ce que nous pouvons pour égaliser les conditions de vie des
différents groupes.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: SDO - 2

Start of Block: SDO - 3


pes19_sdo3 Group equality should be our ideal.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                        434
pes19_sdo3 L'égalité entre les groupes devrait être un idéal à atteindre.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: SDO - 3

Start of Block: SDO - 4


pes19_sdo4 It's probably a good thing that certain groups are at the top and other groups are at
the bottom.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                            435
pes19_sdo4 C'est probablement une bonne chose que certains groupes soient avantagés et
d'autres groupes soient désavantagés.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: SDO - 4



   9.3.41    How much should be done for <group>


NOTE: The order of the four “How much should be done for X” questions
was randomized.


Start of Block: How much should be done for... racial minorities


pes19_donerm How much do you think should be done for racial minorities?

   o Much more (1)
   o Somewhat more (2)
   o About the same as now (3)
   o Somewhat less (4)
   o Much less (5)
   o Don't know/ Prefer not to answer (6)

                                                                                     436
pes19_donerm Selon vous, combien devrait être fait pour les minorités raciales?

   o Beaucoup plus (1)
   o Un peu plus (2)
   o Ni plus ni moins (3)
   o Un peu moins (4)
   o Beaucoup moins (5)
   o Je ne sais pas / Préfère ne pas répondre (6)
End of Block: How much should be done for... racial minorities

Start of Block: How much should be done for... women


pes19_donew How much do you think should be done for women?

   o Much more (1)
   o Somewhat more (2)
   o About the same as now (3)
   o Somewhat less (4)
   o Much less (5)
   o Don't know/ Prefer not to answer (6)




                                                                                  437
pes19_donew Selon vous, combien devrait être fait pour les femmes?

   o Beaucoup plus (1)
   o Un peu plus (2)
   o Ni plus ni moins (3)
   o Un peu moins (4)
   o Beaucoup moins (5)
   o Je ne sais pas / Préfère ne pas répondre (6)
End of Block: How much should be done for... women

Start of Block: How much should be done for... gays and lesbians


pes19_donegl How much do you think should be done for gays and lesbians?

   o Much more (1)
   o Somewhat more (2)
   o About the same as now (3)
   o Somewhat less (4)
   o Much less (5)
   o Don't know/ Prefer not to answer (6)




                                                                           438
pes19_donegl Selon vous, combien devrait être fait pour les gais et lesbiennes?

   o Beaucoup plus (1)
   o Un peu plus (2)
   o Ni plus ni moins (3)
   o Un peu moins (4)
   o Beaucoup moins (5)
   o Je ne sais pas / Préfère ne pas répondre (6)
End of Block: How much should be done for... gays and lesbians

Start of Block: How much should be done for... quebec


pes19_doneqc How much do you think should be done for Quebec?

   o Much more (1)
   o Somewhat more (2)
   o About the same as now (3)
   o Somewhat less (4)
   o Much less (5)
   o Don't know/ Prefer not to answer (6)




                                                                                  439
pes19_doneqc Selon vous, combien devrait être fait pour le Québec?

   o Beaucoup plus (1)
   o Un peu plus (2)
   o Ni plus ni moins (3)
   o Un peu moins (4)
   o Beaucoup moins (5)
   o Je ne sais pas / Préfère ne pas répondre (6)
End of Block: How much should be done for... quebec



   9.3.42     Taxes


NOTE: pes19_taxes was set to receive a split sample of 50% (1/2), to
make room in the survey for more questions. Whether a respondent was
assigned to receive pes19_taxes was randomly determined in the Survey
Flow by setting the embedded data field split_taxes to either 0 or 1.
If split_taxes was equal to 1, they were assigned to receive
pes19_taxes. split_taxes can be used to filter the dataset to only
respondents that were assigned to receive pes19_taxes.


Start of Block: Other: taxes




                                                                     440
pes19_taxes How much should each of the following pay in taxes?
                                                                                 Don't
                                         About the
                 Much       Somewhat                 Somewhat     Much less   know/Prefer
                                         same as
                more (1)     more (2)                 less (4)       (5)         not to
                                          now (3)
                                                                               answer (6)

    Small
 business (1)       o            o           o            o           o            o
     Big
 Corporations
     (2)            o            o           o            o           o            o
 The Middle
  Class (3)         o            o           o            o           o            o
   Wealthy
  Canadians
     (4)            o            o           o            o           o            o
    Poor
  Canadians
     (5)            o            o           o            o           o            o




                                                                                       441
pes19_taxes Combien d'impôts devraient payer les suivants?
                                                                               Ne sais
                                        À peu près                               pas/
                 Beaucoup    Un peu     autant que     Un peu     Beaucoup    Préfère ne
                  plus (1)   plus (2)   maintenant    moins (4)   moins (5)      pas
                                            (3)                               répondre
                                                                                  (6)
   Petites
 entreprises
     (1)              o          o           o               o        o           o
   Grandes
 corporations
     (2)              o          o           o               o        o           o
  La classe
  moyenne
     (3)              o          o           o               o        o           o
    Les
 Canadiens
 riches (4)           o          o           o               o        o           o
    Les
 Canadiens
 pauvres (5)          o          o           o               o        o           o

End of Block: Other: taxes



   9.3.43       Abortion

NOTE: The questions on abortion were set to receive a split sample of
50% (1/2), to make room in the survey for more questions. Because
there were 6 alternate versions of the abortion questions, of which
allocated respondents received one, this results in 1/12 of the PES
sample receiving a given version of the abortion questions. Whether a
respondent was assigned to receive one of the abortion questions was
randomly determined in the Survey Flow by setting the embedded data
field split_abortion to either 0 or 1. If split_abortion was equal to
1, they were assigned to receive QNAME. split_abortion can be used to
filter the dataset to only respondents that were assigned to receive
one of the abortion questions.




                                                                                     442
Start of Block: Other: Abortion 1


pes19_abort1 Should abortion be banned?

   o Yes (1)
   o No (2)
   o Don't know/ Prefer not to answer (3)
pes19_abort1 L'avortement devrait-il être interdit?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)

pes19_abort2 Should abortion be banned?

   o Yes (1)
   o In some circumstances (2)
   o No (3)
   o Don't know/ Prefer not to answer (4)
pes19_abort2 L'avortement devrait-il être interdit?

   o Oui (1)
   o Dans certaines circonstances (2)
   o Non (3)
   o Je ne sais pas/ Préfère ne pas répondre (4)

                                                      443
pes19_abort3 How much do you agree or disagree with the following statement.

There should be more restrictions on abortion.

    o Strongly disagree (1)
    o Somewhat disagree (2)
    o Neither agree nor disagree (3)
    o Somewhat agree (4)
    o Strongly agree (5)
    o Don't know/ Prefer not to answer (6)
pes19_abort3 À quel point êtes-vous en accord ou désaccord avec l'énoncé suivant?


Il devrait y avoir plus de restrictions sur l'avortement.

    o Fortement en désaccord (1)
    o Plutôt en désaccord (2)
    o Ni en désaccord, ni en accord (3)
    o Plutôt en accord (4)
    o Fortement en accord (5)
    o Je ne sais pas/ Préfère ne pas répondre (6)




                                                                                    444
pes19_abort4 Now we would like to get your views on abortion. Of the following three positions,
which is closest to your own opinion?

   o Abortion should be a matter of the woman’s personal choice (21)
   o Abortion should never be permitted (22)
   o Abortion should be permitted only after need has been established by a doctor (23)
   o Don't know/ Prefer not to answer (24)
pes19_abort4 Nous aimerions connaitre votre opinion au sujet de l'avortement. Parmis les trois
énoncés suivants, lequel est le plus proche de votre propre position?

   o L'avortement est un choix personnel fait par une femme. (21)
   o L'avortement ne devrait jamais être permis (22)
   o L'avortement devrait seulement être permis si un docteur estime qu'il est nécessaire.
   (23)

   o Je ne sais pas/ Préfère ne pas répondre (24)

pes19_abort5 And now a question on abortion. How easy or difficult should it be for women to
get an abortion?

   o Very easy (1)
   o Somewhat easy (2)
   o Somewhat difficult (3)
   o Very difficult (4)
   o Don't know/ Prefer not to answer (5)


                                                                                            445
pes19_abort5 Et maintenant une question sur l'avortement. À quel point est-il facile ou difficile
pour les femmes de se faire avorter?

   o Très facile (1)
   o Plutôt facile (2)
   o Plutôt difficile (3)
   o Très difficile (4)
   o Je ne sais pas/ Préfère ne pas répondre (5)

pes19_abort6 How much do you agree or disagree with the following statement.

The decision to have an abortion should be the responsibility of the pregnant woman.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_abort6 À quel point êtes-vous en accord ou désaccord avec l'énoncé suivant?




                                                                                               446
La décision d'avorter devrait être celle de la femme enceinte.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Other: Abortion 1

Start of Block: Likert section 3 intro


pes19_likert_intro3 How much do you agree or disagree with the following statements? Please
click → to see first statement.

pes19_likert_intro3 À quel point êtes-vous en accord ou en désaccord avec les énoncés
suivants? Cliquez → pour voir le premier énoncé.


End of Block: Likert section 3 intro




                                                                                        447
   9.3.44     International trade

NOTE: pes19_trade was set to receive a split sample of 50% (1/2), to
make room in the survey for more questions. Whether a respondent was
assigned to receive pes19_trade was randomly determined in the Survey
Flow by setting the embedded data field split_trade to either 0 or 1.
If split_trade was equal to 1, they were assigned to receive
pes19_trade. split_trade can be used to filter the dataset to only
respondents that were assigned to receive pes19_trade.


Start of Block: Statement: International Trade


pes19_trade International trade creates more jobs in Canada than it destroys.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_trade Le commerce international crée plus d'emplois au Canada qu'il n'en détruit.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)

                                                                                          448
End of Block: Statement: International Trade



   9.3.45     Private sector and jobs


Start of Block: Statement: Private sector and jobs


pes19_privjobs The government should leave it entirely to the private sector to create jobs.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_privjobs Le gouvernement devrait laisser au secteur privé l'entière responsabilité de
créer des emplois.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Statement: Private sector and jobs




                                                                                               449
   9.3.46    Role of government in inequality

Start of Block: Statements: Government should act to reduce inequality


pes19_govt_act_ineq The government should take measures to reduce differences in income
levels.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_govt_act_ineq Le gouvernement devrait prendre des mesures pour réduire les écarts
entre les niveaux de revenus

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Statements: Government should act to reduce inequality



   9.3.47    Deservingness




                                                                                          450
Start of Block: Statements: Deservingness


pes19_deserve1 If people really want to work, they can find a job.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_deserve1 Si les gens veulent vraiment travailler, ils peuvent trouver un emploi.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
Page Break




                                                                                         451
pes19_deserve2 The welfare state makes people less willing to look after themselves.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_deserve2 Les programmes sociaux incitent les gens à moins se débrouiller par eux-
même

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Statements: Deservingness



   9.3.48     Get ahead & Govt should


NOTE: pes19_blame and pes19_stdofliving were set to receive a split
sample of 50% (1/2), to make room in the survey for more questions.
Whether a respondent was assigned to receive pes19_blame and
pes19_stdofliving was randomly determined in the Survey Flow by
setting the embedded data field split_getahead to either 0 or 1. If



                                                                                          452
split_getahead was equal to 1, they were assigned to receive
pes19_blame and pes19_stdofliving. split_getahead can be used to
filter the dataset to only respondents that were assigned to receive
pes19_blame and pes19_stdofliving.


Start of Block: Get ahead & Govt should


pes19_blame People who don't get ahead should blame themselves, not the system.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_blame Ceux qui ne réussissent pas dans la vie devraient se blâmer eux-mêmes, pas le
système.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
Page Break




                                                                                       453
pes19_stdofliving The government should:

   o See to it that everyone has a decent standard of living (1)
   o Leave people to get ahead on their own (2)
   o Don't know/ Prefer not to answer (3)
pes19_stdofliving Le gouvernement devrait:

   o Voir à ce que tout le monde ait un niveau de vie décent (1)
   o Laisser les gens avancer par eux-mêmes (2)
   o Je ne sais pas / Préfère ne pas répondre (3)
End of Block: Get ahead & Govt should



   9.3.49     Trust


Start of Block: Trust


pes19_trust Generally speaking would you say that most people can be trusted, or that you
need to be very careful when dealing with people?

   o Most people can be trusted (1)
   o You need to be very careful when dealing with people (2)
   o Don't know/ Prefer not to answer (3)




                                                                                            454
pes19_trust En général, diriez-vous qu'on peut faire confiance à la plupart des gens, ou qu'on
doit être très prudent dans nos relations avec les autres.

   o On peut faire confiance à la plupart des gens (1)
   o On devrait être très prudent dans nos relations avec les autres (2)
   o Je ne sais pas / Préfère ne pas répondre (3)
End of Block: Trust



   9.3.50     Inequality


Start of Block: Inequality


pes19_inequal Is income inequality a big problem in Canada?

   o Definitely yes (1)
   o Probably yes (2)
   o Not sure (3)
   o Probably not (4)
   o Definitely not (5)
   o Don't know/ Prefer not to answer (6)




                                                                                            455
pes19_inequal Est-ce que les inégalités de revenu sont un problème important au Canada?

   o Définitivement oui (1)
   o Probablement oui (2)
   o Pas certain (3)
   o Probablement pas (4)
   o Définitivement pas (5)
   o Je ne sais pas / Préfère ne pas répondre (6)
End of Block: Inequality

Start of Block: Inequality gap


pes19_gap How much do you think should be done to reduce the gap between the rich and the
poor in Canada?

   o Much more (1)
   o Somewhat more (2)
   o About the same as now (3)
   o Somewhat less (4)
   o Much less (5)
   o Don't know/ Prefer not to answer (6)




                                                                                          456
pes19_gap Que devrait-on faire pour réduire les écarts entre les riches et les pauvres au
Canada?

   o Beaucoup plus (1)
   o Un peu plus (2)
   o Ni plus ni moins (3)
   o Un peu moins (4)
   o Beaucoup moins (5)
   o Je ne sais pas / Préfère ne pas répondre (6)
End of Block: Inequality gap



   9.3.51     Stronger Federal or Provincial government


Start of Block: Strong fed or prov govt


pes19_provfed Which do you prefer:

   o A strong federal government (1)
   o More power to the provincial governments (2)
   o Don't know/ Prefer not to answer (3)
pes19_provfed Lequel préfèrez-vous:

   o Un gouvernement fédéral fort (1)
   o Plus de pouvoir accordé aux gouvernements provinciaux (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)

                                                                                            457
End of Block: Strong fed or prov govt

Start of Block: Likert section 4 intro


pes19_likert_intro4 How much do you agree or disagree with the following statements? Please
click → to see first statement.

pes19_likert_intro4 À quel point êtes-vous en accord ou en désaccord avec les énoncés
suivants? Cliquez → pour voir le premier énoncé.


End of Block: Likert section 4 intro




                                                                                        458
   9.3.52     Sexism

NOTE: The questions on sexism: pes19_hostile1, pes19_hostile2,
pes19_hostile3, pes19_benevolent1, pes19_benevolent2, and
pes19_benevolent3, were set to receive a split sample of 50% (1/2), to
make room in the survey for more questions. Whether a respondent was
assigned to receive the sexism questions was randomly determined in
the Survey Flow by setting the embedded data field split_sexism to
either 0 or 1. If split_sexism was equal to 1, they were assigned to
receive the sexism questions. split_sexism can be used to filter the
dataset to only respondents that were assigned to receive the sexism
questions.

The order of the six sexism questions was fully randomized.


Start of Block: Other: statements: Sexism - 1


pes19_hostile1 Most women fail to appreciate all that men do for them.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                         459
pes19_hostile1 La plupart des femmes n'apprécient pas tout ce que les hommes font pour elles.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Other: statements: Sexism - 1

Start of Block: Other: statements: Sexism - 2


pes19_hostile2 Women seek to gain power by getting control over men.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                         460
pes19_hostile2 Les femmes cherchent à gagner du pouvoir en contrôlant les hommes.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Other: statements: Sexism - 2

Start of Block: Other: statements: Sexism - 3


pes19_hostile3 Most women interpret innocent remarks or acts as being sexist.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                    461
pes19_hostile3 La plupart des femmes qualifient de sexistes des commentaires ou des actions
inoffensives.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Other: statements: Sexism - 3

Start of Block: Other: statements: Sexism - 4


pes19_benevolent1 Women should be cherished and protected by men.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                        462
pes19_benevolent1 Les femmes doivent être chéries et protégées par les hommes.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Other: statements: Sexism - 4

Start of Block: Other: statements: Sexism - 5


pes19_benevolent2 Many women have a quality of purity that few men possess.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                 463
pes19_benevolent2 Beaucoup de femmes ont une qualité de pureté que peu d'hommes
possèdent.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Other: statements: Sexism - 5

Start of Block: Other: statements: Sexism - 6


pes19_benevolent3 A good woman ought to be set on a pedestal by her man.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                  464
pes19_benevolent3 Une bonne femme devrait être placée sur un piédestal par son homme.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Other: statements: Sexism - 6



   9.3.53     Climate Change


Start of Block: Climate change


pes19_cc1 Do you think that climate change is happening?

   o Yes (1)
   o No (2)
   o Don't know/ Prefer not to answer (3)
pes19_cc1 Pensez-vous que les changements climatiques se produisent réellement?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)


                                                                                        465
Page Break


Display This Question:
    If Do you think that climate change is happening? = Yes


pes19_cc2 What do you think is the main cause of climate change?

   o Human activities such as burning fossil fuels for energy (1)
   o Natural changes in the environment (2)
   o Other (3) ________________________________________________
   o Don't know/ Prefer not to answer (4)
pes19_cc2 Quelle est la cause des changements climatiques selon vous?

   o Causés principalement par des activités humaines telles que la combustion des
   énergies fossiles (1)

   o Causés principalement par des changements naturels dans l'environnement (2)
   o Autre (3) ________________________________________________
   o Je ne sais pas/ Préfère ne pas répondre (4)
End of Block: Climate change



   9.3.54      Party identification


NOTE: There were two alternate party identification sections: the CSES
wording, consisting of pes19_pid_close, pes19_little_close, pes19_pid,
which were followed by pes19_pid_strength; and the traditional
wording, pes19_pidtrad, which was followed by pes19_pidtradstrong.
Respondents who had received the earlier CSES branch (splitsample =
CSES) received the CSES versions, while the respondents that received
the other branch (splitsample = modules) received the traditional
wording.



                                                                                     466
Start of Block: CSES Party identification


pes19_pid_close Do you usually think of yourself as close to any particular federal political
party?

   o Yes (1)
   o No (2)
   o Don't know/ Prefer not to answer (3)
pes19_pid_close                Vous considérez-vous habituellement comme étant proche d’un
parti politique fédéral?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/Préfère ne pas répondre (3)
Page Break




                                                                                                467
Display This Question:
    If Do you usually think of yourself as close to any particular federal political party? = No


pes19_little_close Do you feel yourself a little closer to one of the political parties than the
others?

   o Yes (1)
   o No (2)
   o Don't know / Prefer not to answer (3)
pes19_little_close              Estimez-vous que vous êtes un peu plus proche de l’un des
partis politiques fédéraux que des autres?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)
Page Break




                                                                                                   468
Display This Question:
    If Do you usually think of yourself as close to any particular federal political party? = Yes
    Or Do you feel yourself a little closer to one of the political parties than the others? = Yes




pes19_pid Which party do you feel closest to?

    o Liberal Party (1)
    o Conservative Party (2)
    o NDP (3)
In which province or territory are you currently living? = Quebec

    o Bloc Québécois (4)
    o Green Party (7)
    o People's Party (8)
    o Other (specify) (5) ________________________________________________
    o Don't know/ Prefer not to answer (6)




                                                                                                     469
pes19_pid De quel parti vous sentez-vous le plus proche?

    o Parti libéral (1)
    o Parti conservateur (2)
    o NPD (3)
In which province or territory are you currently living? = Quebec

    o Bloc québécois (4)
    o Parti vert (7)
    o Parti populaire (8)
    o Autre (spécifiez) (5) ________________________________________________
    o Je ne sais pas/ Préfère ne pas répondre (6)
Page Break




                                                                               470
Display This Question:
    If Which party do you feel closest to? = Liberal Party
    Or Which party do you feel closest to? = Conservative Party
    Or Which party do you feel closest to? = NDP
    Or Which party do you feel closest to? = Bloc Québécois
    Or Which party do you feel closest to? = Green Party
    Or Which party do you feel closest to? = People's Party
    Or Which party do you feel closest to? = Other (specify)


pes19_pid_strength How close do you feel to this party?

   o Very close (1)
   o Somewhat close (2)
   o Not very close (3)
   o Don't know/ Prefer not to answer (4)
pes19_pid_strength À quel point vous sentez-vous proche de ce parti?

   o Très proche (1)
   o Plutôt proche (2)
   o Pas très proche (3)
   o Je ne sais pas/ Préfère ne pas répondre (4)
End of Block: CSES Party identification

Start of Block: Party ID and membership part 1




                                                                       471
pes19_pidtrad In federal politics, do you usually think of yourself as a:

    o Liberal (1)
    o Conservative (2)
    o NDP (3)
In which province or territory are you currently living? = Quebec

    o Bloc Québécois (4)
    o Green (5)
    o People’s Party (6)
    o Another party (please specify) (7)
    ________________________________________________

    o None of these (8)
    o Don't know/ Prefer not to answer (9)




                                                                            472
pes19_pidtrad En politique fédérale, vous considérez-vous habituellement comme étant :

    o Libéral (1)
    o Conservateur (2)
    o NPD (3)
In which province or territory are you currently living? = Quebec

    o Bloc québécois (4)
    o Parti vert (5)
    o Parti populaire du Canada (6)
    o Un autre parti (Veuillez spécifier) (7)
    ________________________________________________

    o Aucun de ces partis (8)
    o Je ne sais pas/Préfère ne pas répondre (9)
End of Block: Party ID and membership part 1


Note: After they responded with their federal party identification,
the relevant party was piped into the relevant follow-up questions.


Start of Block: Party ID and membership part 2
Display This Question:
    If In federal politics, do you usually think of yourself as a: != None of these
    And In federal politics, do you usually think of yourself as a: != Don't know/ Prefer not to answer




                                                                                                          473
pes19_pidtradstrong How strongly ${e://Field/pid_en}${pes19_pidtrad/ChoiceTextEntryValue/7}
do you feel?

   o Very strongly (1)
   o Fairly strongly (2)
   o Not very strongly (3)
   o Don't know/ Prefer not to answer (4)
pes19_pidtradstrong À quel point vous sentez-vous proche
du ${e://Field/pid_party_fr}${pes19_pidtrad/ChoiceTextEntryValue/7}?

   o Très fortement (1)
   o Fortement (2)
   o Pas très fortement (3)
   o Je ne sais pas/Préfère ne pas répondre (4)
End of Block: Party ID and membership part 2



   9.3.55     Affective party identification


Start of Block: Affective PID




                                                                                        474
Display This Question:
        If In federal politics, do you usually think of yourself as a: = Liberal
        Or In federal politics, do you usually think of yourself as a: = Conservative
        Or In federal politics, do you usually think of yourself as a: = NDP
        Or In federal politics, do you usually think of yourself as a: = Bloc Québécois
        Or In federal politics, do you usually think of yourself as a: = Green
        Or In federal politics, do you usually think of yourself as a: = People’s Party
Or If
        Which party do you feel closest to? = Liberal Party
        Or Which party do you feel closest to? = Conservative Party
        Or Which party do you feel closest to? = NDP
        Or Which party do you feel closest to? = Bloc Québécois
        Or Which party do you feel closest to? = Green Party
        Or Which party do you feel closest to? = People's Party




                                                                                          475
pes19_affective Now thinking about the party you feel closest to, how often do you think about it
in the following ways?
                                                                                        Don't
                                                                                       know/
                                         Sometimes
                            Never (1)                     Often (3)   Always (4) Prefer not
                                              (2)
                                                                                     to answer
                                                                                         (5)
   When people criticize
               the
 ${e://Field/pid_party_en},
   it feels like a personal       o             o              o            o             o
           insult. (1)
   When I meet someone
      who supports the
 ${e://Field/pid_party_en}
 I feel connected with this       o             o              o            o             o
         person. (2)
  When I speak about the
 ${e://Field/pid_party_en},
 I refer to it as "my party".
               (3)
                                  o             o              o            o             o
  When people praise the
 ${e://Field/pid_party_en},
  it makes me feel good.
             (4)
                                  o             o              o            o             o




                                                                                             476
pes19_affective Maintenant, en pensant au parti auquel vous vous sentez le plus proche, à
quelle fréquence pensez vous de la manière suivante?
                                                                                   Je ne sais
                                                      Souvent      Toujours       pas/préfère
                          Jamais (1) Parfois (2)
                                                         (3)          (4)           ne pas
                                                                                 répondre (5)
  Lorsque les individus
         critiquent le
 ${e://Field/pid_party_fr},
   je le ressens comme
 une insulte personnelle.
                                o            o            o             o             o
               (1)
   Lorsque je rencontre
 quelqu'un qui supporte
             le
 ${e://Field/pid_party_fr},
  je me sens connecté à
                                o            o            o             o             o
      cet individu. (2)
     Lorsque je parle du
 ${e://Field/pid_party_fr},
  j’y réfère comme "mon
          parti". (3)
                                o            o            o             o             o
  Lorsque des individus
     complimentent le
 ${e://Field/pid_party_fr},
   je me sens bien. (4)
                                o            o            o             o             o

End of Block: Affective PID



   9.3.56      Quebec questions


NOTE: These questions, pes19_langQC, pes19_cultureQC , pes19_qclang,
and pes19_qcsol, were only received by respondents in Quebec.


Start of Block: Quebec: French Language & culture threat




                                                                                          477
pes19_langQC In your opinion, is the French language threatened in Quebec?

   o Yes (1)
   o No (2)
   o Don’t know/ Prefer not to answer (3)
pes19_langQC Selon vous, la langue française est-elle menacée au Québec?

   o oui (1)
   o Non (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)
Page Break




                                                                             478
pes19_cultureQC In your opinion, is the French culture threatened in Quebec?

   o Yes (1)
   o No (2)
   o Don’t know/ Prefer not to answer (3)
pes19_cultureQC Selon vous, la culture française est-elle menacée au Québec?

   o Oui (1)
   o Non (2)
   o Je ne sais pas/ Préfère ne pas répondre (3)
End of Block: Quebec: French Language & culture threat

Start of Block: Quebec seperation


pes19_qclang If Quebec separates from Canada, do you think that the situation of the French
language in Quebec will...

   o Get better (1)
   o Get worse (2)
   o Stay about the same as now (3)
   o Don't know/ Prefer not to answer (4)




                                                                                          479
pes19_qclang Si le Québec se sépare du Canada, pensez-vous que la situation de la langue
française au Québec...

   o Va s'améliorer (1)
   o Va s'aggraver (2)
   o Restera à peu près la même (3)
   o Je ne sais pas/ Préfère ne pas répondre (4)
Page Break




                                                                                       480
pes19_qcsol If Quebec separates from Canada, do you think your standard of living will...

   o Get better (1)
   o Get worse (2)
   o Stay about the same as now (3)
   o Don't know/ Prefer not to answer (4)
pes19_qcsol Si le Québec se sépare du Canada, croyez-vous que votre niveau de vie...

   o Va s'améliorer (1)
   o Va s'aggraver (2)
   o Restera à peu près le même (3)
   o Je ne sais pas/ Préfère ne pas répondre (4)
End of Block: Quebec seperation

Start of Block: Likert section 5 intro


pes19_likert_intro5 How much do you agree or disagree with the following statements? Please
click → to see first statement.

pes19_likert_intro5 À quel point êtes-vous en accord ou désaccord avec les énoncés suivants?


End of Block: Likert section 5 intro



   9.3.57     New lifestyles


Start of Block: Statements: Newer lifestyles




                                                                                            481
pes19_newerlife Newer lifestyles are contributing to the breakdown of our society.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)
pes19_newerlife Les nouveaux modes de vie contribuent à la dégradation de notre société.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Statements: Newer lifestyles




                                                                                           482
   9.3.58     Life satisfaction

NOTE: pes19_happy and pes19_satisfied was set to receive a split
sample of 50% (1/2), to make room in the survey for more questions.
Whether a respondent was assigned to receive pes19_happy and
pes19_satisfied was randomly determined in the Survey Flow by setting
the embedded data field split_lifesat to either 0 or 1. If
split_lifesat was equal to 1, they were assigned to receive
pes19_happy and pes19_satisfied. split_lifesat can be used to filter
the dataset to only respondents that were assigned to receive
pes19_happy and pes19_satisfied.


Start of Block: Other: statements: Life Satisfaction


pes19_happy In most ways, my life is close to my ideal.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                    483
pes19_happy À bien des égards, ma vie est proche de mon idéal.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt d'accord (4)
   o Fortement d'accord (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
Page Break




                                                                 484
pes19_satisfied
I am satisfied with my life.

    o Strongly disagree (1)
    o Somewhat disagree (2)
    o Neither agree nor disagree (3)
    o Somewhat agree (4)
    o Strongly agree (5)
    o Don't know/ Prefer not to answer (6)
pes19_satisfied
Je suis satisfait de ma vie.

    o Fortement en désaccord (1)
    o Plutôt en désaccord (2)
    o Ni en accord, ni en désaccord (3)
    o Plutôt d'accord (4)
    o Fortement d'accord (5)
    o Je ne sais pas/ Préfère ne pas répondre (6)
End of Block: Other: statements: Life Satisfaction




                                                     485
   9.3.59      Cognition

NOTE: pes19_cognition was set to receive a split sample of 50% (1/2),
to make room in the survey for more questions. Whether a respondent
was assigned to receive pes19_cognition was randomly determined in the
Survey Flow by setting the embedded data field split_responsibility to
either 0 or 1. If split_responsibility was equal to 1, they were
assigned to receive pes19_cognition. split_responsibility can be used
to filter the dataset to only respondents that were assigned to
receive pes19_cognition.


Start of Block: Other: statements: responsibility


pes19_cognition I like to have responsibility for handling situations that require a lot of thinking.

   o Strongly disagree (1)
   o Somewhat disagree (2)
   o Neither agree nor disagree (3)
   o Somewhat agree (4)
   o Strongly agree (5)
   o Don't know/ Prefer not to answer (6)




                                                                                                  486
pes19_cognition J'aime avoir la responsabilité de gérer des situations qui nécessitent beaucoup
de réflexion.

   o Fortement en désaccord (1)
   o Plutôt en désaccord (2)
   o Ni en accord, ni en désaccord (3)
   o Plutôt en accord (4)
   o Fortement en accord (5)
   o Je ne sais pas/Préfère ne pas répondre (6)
End of Block: Other: statements: responsibility



   9.3.60     Gender identity

NOTE: pes19_feminine and pes19_masculine were set to receive a split
sample of 50% (1/2), to make room in the survey for more questions.
Whether a respondent was assigned to receive pes19_feminine and
pes19_masculine was randomly determined in the Survey Flow by setting
the embedded data field split_gender_id to either 0 or 1. If
split_gender_id was equal to 1, they were assigned to receive
pes19_feminine and pes19_masculine. split_gender_id can be used to
filter the dataset to only respondents that were assigned to receive
pes19_feminine and pes19_masculine.

Also note that the order of pes19_feminine and pes19_masculine was
randomized.


Start of Block: Gender ID - feminine



pes19_feminine How much do you identity as feminine on a scale from 0 to 100, where 0
means not at all feminine and 100 means very feminine.




                                                                                           487
If you do not know, or prefer not to answer, please click →
                                                   Not feminine at all       Very feminine

                                                 0   10 20 30 40 50 60 70 80 90 100

                   &nbsp ()




pes19_feminine À quel point vous estimez-vous comme féminine sur une échelle de 0 à
100, où 0 signifie que vous n'êtes pas du tout féminine et 100 que vous êtes très féminine.
Si vous ne savez pas, ou préférez ne pas répondre, veuillez appuyer sur →
                                                  Pas du tout féminine        Très féminine

                                                 0   10 20 30 40 50 60 70 80 90 100

                   &nbsp ()




End of Block: Gender ID - feminine

Start of Block: Gender ID - masculine



pes19_masculine How much do you identity as masculine on a scale from 0 to 100, where 0
means not at all masculine and 100 means very masculine.

If you do not know, or prefer not to answer, please click →
                                                  Not masculine at all      Very masculine

                                                 0   10 20 30 40 50 60 70 80 90 100

                   &nbsp ()




pes19_masculine À quel point vous estimez-vous comme masculin sur une échelle de 0 à 100,
où 0 signifie que vous n'êtes pas du tout masculin et 100 que vous êtes très masculin.
Si vous ne savez pas, ou préférez ne pas répondre, veuillez appuyer sur →
                                                  Pas du tout masculin       Très masculin

                                                 0   10 20 30 40 50 60 70 80 90 100


                                                                                              488
                   &nbsp ()




End of Block: Gender ID - masculine


   9.3.61      Big 5

NOTE: pes19_big5 was set to receive a split sample of 50% (1/2), to
make room in the survey for more questions. Whether a respondent was
assigned to receive pes19_big5 was randomly determined in the Survey
Flow by setting the embedded data field split_big5 to either 0 or 1.
If split_big5 was equal to 1, they were assigned to receive
pes19_big5. split_big5 can be used to filter the dataset to only
respondents that were assigned to receive pes19_big5.


Start of Block: Big 5 Word descriptions



pes19_big5 We’re interested in how you see yourself. Please indicate how well the following
pair of words describes you, even if one word describes you better than the other. On the left, 1
means those words describe you extremely poorly; on the right, 7 means those words describe
you extremely well. Please use any number.

If you do not know, or prefer not to answer, please click →
                                                      Describes you           Describes you
                                                     extremely poorly         extremely well

                                                   1      2      3      4      5      6        7




                                                                                               489
           Extraverted/enthusiastic ()

             Critical/quarrelsome ()

         Dependable/self-disciplined ()

             Anxious/easily upset ()

     Open to new experiences/complex ()

                Reserved/quiet ()

              Sympathetic/warm ()

            Disorganized/careless ()

           Calm/emotionally stable ()

           Conventional/uncreative ()




pes19_big5 Nous souhaiterions en apprendre plus sur la façon dont vous vous percevez.
Indiquez si ces mots vous décrivent bien ou non, même si un des mots vous décrit mieux que
l'autre. Sur la gauche, 1 signifie que ces mots vous décrivent très mal; sur la droite, 7 signifie
que ces mots vous décrivent très bien. Utiliser n'importe quel nombre.

           Si vous ne le savez pas ou si vous préférez ne pas répondre, veuillez cliquer sur →
                                                  Vous décrit très mal   Vous décrit très bien

                                                     1      2      3      4       5      6      7




                                                                                                490
          Extraverti/enthousiaste ()

            Critique/querelleur ()

             Fiable/discipliné ()

       Anxieux/facilement contrarié ()

 Ouvert aux nouvelles expériences/complexe
                     ()
            Réservé/silencieux ()

         Sympathique/chaleureux ()

          Désorganisé/insouciant ()

      Calme/stable émotionnellement ()

         Conventionel/peu créatif ()




End of Block: Big 5 Word descriptions




                                             491
   9.3.62      Health initial


Start of Block: Health - initial


pes19_health Compared to other people your age, how would you describe your health?

   o Excellent (1)
   o Very good (2)
   o Fair (3)
   o Poor (4)
   o Don't know/ Prefer not to answer (5)
pes19_health Comment décririez-vous votre état de santé par rapport aux autres personnes de
votre âge?

   o Excellent (1)
   o Très bien (2)
   o Moyen (3)
   o Pauvre (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
End of Block: Health - initial




                                                                                        492
   9.3.63     Health follow-ups

NOTE: pes19_phealth and pes19_mhealth were set to receive a split
sample of 50% (1/2), to make room in the survey for more questions.
Whether a respondent was assigned to receive pes19_phealth and
pes19_mhealth was randomly determined in the Survey Flow by setting
the embedded data field split_health_followups to either 0 or 1. If
split_health_followups was equal to 1, they were assigned to receive
pes19_phealth and pes19_mhealth. split_health_followups can be used to
filter the dataset to only respondents that were assigned to receive
pes19_phealth and pes19_mhealth.

Also note that the order of pes19_phealth and pes19_mhealth was
randomized.



Start of Block: Health - follow-up physical


pes19_phealth Compared to other people your age, how would you describe your physical
health?

   o Excellent (1)
   o Very good (2)
   o Fair (3)
   o Poor (4)
   o Don't know/ Prefer not to answer (5)




                                                                                        493
pes19_phealth Comment décririez-vous votre état de santé physique par rapport aux autres
personnes de votre âge?

   o Excellent (1)
   o Très bien (2)
   o Moyenne (3)
   o Pauvre (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
End of Block: Health - follow-up physical

Start of Block: Health - follow-up mental


pes19_mhealth Compared to other people your age, how would you describe your mental
health?

   o Excellent (1)
   o Very good (2)
   o Fair (3)
   o Poor (4)
   o Don't know/ Prefer not to answer (5)




                                                                                       494
pes19_mhealth Comment décririez-vous votre état de santé mentale par rapport aux autres
personnes de votre âge?

   o Excellent (1)
   o Très bien (2)
   o Moyenne (3)
   o Pauvre (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
End of Block: Health - follow-up mental



   9.3.64    Additional demographics


Start of Block: Additional demographics




                                                                                          495
pes19_yob To make sure we are talking to a cross section of Canadians, we need to get a little
information about your background. First, in what year were you born?

   o 1920 (1)
   o 1921 (2)
   o 1922 (3)
   o 1923 (4)
   o 1924 (5)
   o 1925 (6)
   o 1926 (7)
   o 1927 (8)
   o 1928 (9)
   o 1929 (10)
   o 1930 (11)
   o 1931 (12)
   o 1932 (13)
   o 1933 (14)
   o 1934 (15)
   o 1935 (16)
   o 1936 (17)
   o 1937 (18)
   o 1938 (19)
                                                                                          496
o 1939 (20)
o 1940 (21)
o 1941 (22)
o 1942 (23)
o 1943 (24)
o 1944 (25)
o 1945 (26)
o 1946 (27)
o 1947 (28)
o 1948 (29)
o 1949 (30)
o 1950 (31)
o 1951 (32)
o 1952 (33)
o 1953 (34)
o 1954 (35)
o 1955 (36)
o 1956 (37)
o 1957 (38)
o 1958 (39)
              497
o 1959 (40)
o 1960 (41)
o 1961 (42)
o 1962 (43)
o 1963 (44)
o 1964 (45)
o 1965 (46)
o 1966 (47)
o 1967 (48)
o 1968 (49)
o 1969 (50)
o 1970 (51)
o 1971 (52)
o 1972 (53)
o 1973 (54)
o 1974 (55)
o 1975 (56)
o 1976 (57)
o 1977 (58)
o 1978 (59)
              498
o 1979 (60)
o 1980 (61)
o 1981 (62)
o 1982 (63)
o 1983 (64)
o 1984 (65)
o 1985 (66)
o 1986 (67)
o 1987 (68)
o 1988 (69)
o 1989 (70)
o 1990 (71)
o 1991 (72)
o 1992 (73)
o 1993 (74)
o 1994 (75)
o 1995 (76)
o 1996 (77)
o 1997 (78)
o 1998 (79)
              499
o 1999 (80)
o 2000 (81)
o 2001 (82)
o 2002 (83)
o 2003 (84)
o 2004 (85)
o 2005 (86)
o 2006 (87)
o 2007 (88)
o 2008 (89)
o 2009 (90)
o 2010 (91)
o Don't know/ Prefer not to answer (92)




                                          500
pes19_yob Afin d’être certains que nous nous adressons à un échantillon représentatif des
Canadiens, nous avons besoin d’informations de base sur vous. Tout d'abord, en quelle année
êtes-vous né(e)?

   o 1920 (1)
   o 1921 (2)
   o 1922 (3)
   o 1923 (4)
   o 1924 (5)
   o 1925 (6)
   o 1926 (7)
   o 1927 (8)
   o 1928 (9)
   o 1929 (10)
   o 1930 (11)
   o 1931 (12)
   o 1932 (13)
   o 1933 (14)
   o 1934 (15)
   o 1935 (16)
   o 1936 (17)
   o 1937 (18)

                                                                                        501
o 1938 (19)
o 1939 (20)
o 1940 (21)
o 1941 (22)
o 1942 (23)
o 1943 (24)
o 1944 (25)
o 1945 (26)
o 1946 (27)
o 1947 (28)
o 1948 (29)
o 1949 (30)
o 1950 (31)
o 1951 (32)
o 1952 (33)
o 1953 (34)
o 1954 (35)
o 1955 (36)
o 1956 (37)
o 1957 (38)
              502
o 1958 (39)
o 1959 (40)
o 1960 (41)
o 1961 (42)
o 1962 (43)
o 1963 (44)
o 1964 (45)
o 1965 (46)
o 1966 (47)
o 1967 (48)
o 1968 (49)
o 1969 (50)
o 1970 (51)
o 1971 (52)
o 1972 (53)
o 1973 (54)
o 1974 (55)
o 1975 (56)
o 1976 (57)
o 1977 (58)
              503
o 1978 (59)
o 1979 (60)
o 1980 (61)
o 1981 (62)
o 1982 (63)
o 1983 (64)
o 1984 (65)
o 1985 (66)
o 1986 (67)
o 1987 (68)
o 1988 (69)
o 1989 (70)
o 1990 (71)
o 1991 (72)
o 1992 (73)
o 1993 (74)
o 1994 (75)
o 1995 (76)
o 1996 (77)
o 1997 (78)
              504
  o 1998 (79)
  o 1999 (80)
  o 2000 (81)
  o 2001 (82)
  o 2002 (83)
  o 2003 (84)
  o 2004 (85)
  o 2005 (86)
  o 2006 (87)
  o 2007 (88)
  o 2008 (89)
  o 2009 (90)
  o 2010 (91)
  o Je ne sais pas/ Préfère ne pas répondre (92)
Page Break




                                                   505
pes19_month_of_birth In what month were you born?

   o January (1)
   o February (2)
   o March (3)
   o April (4)
   o May (5)
   o June (6)
   o July (7)
   o August (8)
   o September (9)
   o October (10)
   o November (11)
   o December (12)
   o Don't know / Prefer not to answer (13)




                                                    506
pes19_month_of_birth Quel est votre mois de naissance?

   o Janvier (1)
   o Février (2)
   o Mars (3)
   o Avril (4)
   o Mai (5)
   o Juin (6)
   o Juillet (7)
   o Août (8)
   o Septembre (9)
   o Octobre (10)
   o Novembre (11)
   o Décembre (12)
   o Je ne sais pas/ Préfère ne pas répondre (13)
Page Break




                                                         507
pes19_service_freq How often do you attend religious services, excluding special occasions
such as weddings and funerals?

   o Never (1)
   o Once a year (2)
   o Two to eleven times a year (3)
   o Once a month (4)
   o Two or three times a month (5)
   o Once a week or more (6)
   o Don't know / Prefer not to answer (7)
pes19_service_freq À quelle fréquence assistez-vous à des cérémonies religieuses, en
excluant les occasions spéciales telles que les mariages ou les funérailles?

   o Jamais (1)
   o Une fois par an (2)
   o Deux à onze fois par an (3)
   o Une fois par mois (4)
   o Deux ou trois fois par mois (5)
   o Une fois par semaine ou plus (6)
   o Je ne sais pas/ Préfère ne pas répondre (7)
Page Break




                                                                                             508
pes19_parents_born Was either or both of your parents born outside of Canada?

   o Yes (4)
   o No (5)
   o Don't know/ Prefer not to answer (6)
pes19_parents_born Est-ce qu’au moins l'un de vos parents est né à l'extérieur du Canada?

   o Oui (4)
   o Non (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
Page Break




                                                                                            509
pes19_rural_urban Do you live in…

   o A rural area or village (less than1000 people) (1)
   o A small town (more than 1000 people but less than 15K) (2)
   o A middle-sized town (15K-50K people) not attached to a city (3)
   o A suburb of a large town or city (4)
   o A large town or city (more than 50K people) (5)
   o Don't know / Prefer not to answer (6)
pes19_rural_urban Vivez-vous...

   o En milieu rural ou dans un village (moins de 1000 personnes) (1)
   o Dans une petite ville (plus que 1000 mais moins que 15,000 personnes) (2)
   o Dans une ville de taille moyenne (15k-50k personnes) qui n'est pas adjacente à une
   grande fille (3)

   o Dans une banlieue d'une grande ville (4)
   o Dans une grande ville (plus que 50k personnes) (5)
   o Je ne sais pas/ Préfère ne pas répondre (6)
Page Break




                                                                                          510
pes19_lived For how many years have you lived in your current city or community?

   o Less than 1 year (1)
   o 1-3 years (2)
   o 3-10 years (3)
   o More than 10 years (4)
   o Don't know/ Prefer not to answer (5)
pes19_lived Depuis combien d'années vivez-vous dans votre ville ou communauté actuelle?

   o Moins d'un an (1)
   o 1-3 ans (2)
   o 3-10 ans (3)
   o Plus de 10 ans (4)
   o Je ne sais pas / Préfère ne pas répondre (5)
Page Break




                                                                                          511
pes19_follow_pol And how closely do you follow politics on TV, radio, newspapers, or the
Internet?

   o Very closely (1)
   o Fairly closely (2)
   o Not very closely (3)
   o Not at all (4)
   o Don't know/ Prefer not to answer (5)
pes19_follow_pol Et à quel point suivez-vous la politique à la télévision, à la radio, dans les
journaux ou sur l'Internet?

   o De très proche (1)
   o D’assez proche (2)
   o Pas de très près (3)
   o Pas du tout de près (4)
   o Je ne sais pas/ Préfère ne pas répondre (5)
Page Break




                                                                                                  512
pes19_lang Which language do you usually speak at home?

   o English (68)
   o French (69)
   o Aboriginal language (please specify) (70)
   ________________________________________________

   o Arabic (71)
   o Chinese, Cantonese, Mandarin (72)
   o Filipino / Tagalog (73)
   o German (74)
   o Indian, Hindi, Gujarati (75)
   o Italian (76)
   o Korean (77)
   o Pakistani, Punjabi, Urdu (78)
   o Persian, Farsi (79)
   o Russian (80)
   o Spanish (81)
   o Tamil (82)
   o Vietnamese (83)
   o Other (please specify) (84)
   ________________________________________________

   o Don't know/ Prefer not to answer (85)

                                                          513
pes19_lang Quelle est la toute première langue que vous avez apprise et que vous comprenez
encore?

   o Anglais (68)
   o Français (69)
   o Langue autochtone (veuillez préciser) (70)
   ________________________________________________

   o Arabe (71)
   o Chinois, cantonais, mandarin (72)
   o Philippin / tagalog (73)
   o Allemand (74)
   o Indien, Hindi, Gujarati (75)
   o Italien (76)
   o Coréen (77)
   o Pakistanais, Pendjabi, Ourdou (78)
   o Persan, farsi (79)
   o Russe (80)
   o Espagnol (81)
   o Tamil (82)
   o Vietnamien (83)
   o Autre (Veuillez spécifier) (84)
   ________________________________________________

   o Je ne sais pas / Préfère ne pas répondre (85)
                                                                                       514
Page Break



pes19_occ_text What is your main occupation? If you are retired, please enter your former
occupation.

If you do not know, or prefer not to answer, please click →


    ________________________________________________________________

pes19_occ_text Quelle est votre occupation principale? Si vous êtes à la retraite, veuillez, s’il
vous plaît, indiquer votre occupation précédente.

Si vous ne savez pas, ou préférez ne pas répondre, veuillez cliquer sur la flèche →




    ________________________________________________________________



Page Break




                                                                                                515
Display This Question:
     If If What is your main occupation? If you are retired, please enter your former occupation. If you do
not know, or prefer not to answer, please click → &nbsp; Text Response Is Empty


pes19_occ_cat Which of the following broad categories best describes your occupation? If you
do not work currently, select the category of your most recent job.

    o Manager (18)
    o Professional (19)
    o Technician or associate professional (20)
    o Clerical support worker (21)
    o Service or sales worker (22)
    o Skilled agricultural, forestry or fishery worker (23)
    o Craft or related trades worker (24)
    o Plant operator, machine operator, or assembler (25)
    o Cleaner, laborer, or assistant (26)
    o Armed forces (27)
    o Other (please specify) (28) ________________________________________________
    o Don't Know/ Prefer not to answer (29)




                                                                                                        516
pes19_occ_cat Laquelle des grandes catégories suivantes décrit le mieux votre métier? Si vous
ne travaillez pas actuellement, sélectionnez la catégorie de votre dernier emploi.

   o Directeurs, cadres de direction et gérants (18)
   o Professions intellectuelles et scientifiques (19)
   o Professions intermédiaires (20)
   o Employés de type administratif (21)
   o Personnel des services directs aux particuliers, commerçants et vendeurs (22)
   o Agriculteurs et ouvriers qualifiés de l’agriculture, de la sylviculture et de la pêche (23)
   o Métiers qualifiés de l’industrie et de l’artisanat (24)
   o Conducteurs d’installations et de machines, et ouvriers de l’assemblage (25)
   o Professions élémentaires (26)
   o Professions militaires (27)
   o Autre (veuillez spécifier) (28)
   ________________________________________________

   o Je ne sais pas / Préfère ne pas répondre (29)
End of Block: Additional demographics




                                                                                               517
