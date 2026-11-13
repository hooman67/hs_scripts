# HP
we have 9 SKUs and we have 4 environments (gaming, education, office, home). Make sure to have 
examples from each at least 36. 
GPT 5.5
Zach wants to see column A. 



forLegal$;review

  
 



## Deliverables by Sept2 (ideally sooner if we have)
1. Shitong
    -Review the pipeine from Karan to make sure it's hooked up to Seedance (fal ai) and can communicate with Studio.
    -The reference images need pre-processsing (remove face/bodies or sketchify) using nanoBanana
    -Fetch the product reference (using the SKU# provided by re-writer) to fetch the references and pass to the model.  
    -There will be a boolean in the API to denote whether this is an edit task or a generation task.
    -Once the re-writer work is done by Steve/Hooman it needs to be added to the pipeline. GPT 5.6

2. Spencer
    -minor UI work for video generation (shape of the pipeine will be provided by Shitong)
    -feedback mechanism where user sees the generated video, provides feedback, and start another generation cycle.
    -If the user tuggles to the edit mode, they should see the previously generated video. And they will use the existing fields to communicate their changes. 
    -after above is done we'll target, uploading article (and/or storyboard)
    -after above is done, we can consider receiving the reference image/video for a product and showing back to the user.

3. Joshua
    -create motion bank (videos + prompts) for 5 SKUs
    -Figure out exact pre-processing steps needed for the reference images (removing people and bodies or sketchifying). 
    -Figure out if we can get a seedance API that allows faces. 
    -Decide on the exact image model to use for edit (nanoBanan or GPT-2)

4. Steve/Hooman
    **over slack Steve/JOshua/Hooman/Tyler need to align on what the fileds (prompt structure) should be.
    -At the begining, user will see a prompt field. With initial text showing them different structures (scene, angle, etc) that they can fill out. 
    -User clicks generate, and will get back the generation + the expanded prompt. 
    -The simple prompt field will now be replaced with the structure coming out of the re-writer. 
    -The user can edit this and hit generate again. 
    -Similar for the edit workflow. So user will first see the video that was generated, they will tuggle to edit, they will see a prompt field (with some suggestion like edit what you want to change), they can then provide their edit and click generate. They will then see the generated video as well as the expanded prompt (the simple prompt field will be replaced with the structure fields).
    -Re-writer will find the SKU# of any products reference in the prompt (from user) 
    -Re-writer can receive whether this is a generation task or a video edit task.
        Re-writer will still send back the re-written prompt and user can edit before final generation. 

    1. Re-writer receives the pre-processed inputs, as well as the reference images / banks.  

    # 08/31
    1. Experiment with motion transfer using the grid of images insatead of video and prompting. 
    2. Finish curating videos for all SKUs. 


5. Tyler
    -Provide the initial suggestions that we put as text in the prompt field (which after first generation will be replaced by the full structure)
    -Provide the final long-form videos for the 5 (storyboards/articles) that we are demoing. 
        This includes the inputs which will be the images (from storyboard) + the simple prompts that the user should provide. + the actual prompts that were used to generate the shot. 
    -Provide PRD

    





# Humain
1. run media intelligence on our existing videos. Hooman to run. Before Thur. Daniel, Chengchi or Varun.
2. Compute prioratization (with Pranv / Ajinkya)
3. Discuss other POCs. 

# THD action items
## Tyler
1. Pick 5 articles that we should demo to THD 
2. Take an article, don't use any of the visual assets from the article, and try to generate the video for it. 

## Karan
1. Propose and implement a design that takes the inputs that seedance takes and gives video. 
2. And keep the context so user can give feedback on the video.
3. Shitong to hlep Karan with the pipeline / deployment side. A simple wrapper around FAL ai.

## Joshua
1. Take the demo articles, and try to produce video and yo're allowed to look up assets online. 

## Hooman
1. Take the drop in sync iphone shots and try to create the video
    while waiting on Tyler's example.
2. Take the story board sketches and produce the video. 

## Steve
1. Take one of the demo articles, and the reference image of the product, try to produce the video using just prompting.
2. Integrate the human based critiquing. 


# Tickets done by Hooman since 08/20/2026 (meeting with Kaushal on 08/24/2026)
## THD demo 09/18
https://jira.corp.adobe.com/browse/FFDY-7303
https://jira.corp.adobe.com/browse/FFDY-7304
https://jira.corp.adobe.com/browse/FFDY-7309
https://jira.corp.adobe.com/browse/FFDY-7534
https://jira.corp.adobe.com/browse/FFDY-7536
https://jira.corp.adobe.com/browse/FFDY-7583
    * Re-writer work got delayed again because the eval set is not correct:
    Ticket for tyler with Hooman clarification: https://jira.corp.adobe.com/browse/FFDY-7584
    Message informing the team: https://adoberesearch.slack.com/archives/C0BU2ADHCGL/p1788205866125039
https://jira.corp.adobe.com/browse/FFDY-7761
https://jira.corp.adobe.com/browse/FFDY-7820
https://jira.corp.adobe.com/browse/FFDY-7981
https://jira.corp.adobe.com/browse/FFDY-7980
https://jira.corp.adobe.com/browse/FFDY-8029
https://jira.corp.adobe.com/browse/FFDY-8072
https://jira.corp.adobe.com/browse/FFDY-8073
https://jira.corp.adobe.com/browse/FFDY-8064
https://jira.corp.adobe.com/browse/FFDY-8138
https://jira.corp.adobe.com/browse/FFDY-8200
https://jira.corp.adobe.com/browse/FFDY-8271

3D approach for THD
https://jira.corp.adobe.com/browse/FFDY-8454

KDP (hs building POC)
https://jira.corp.adobe.com/browse/FFDY-8567

Mayo (hs did tech validation)
https://jira.corp.adobe.com/browse/FFDY-1425

KDP training through 4.0
https://jira.corp.adobe.com/browse/FFDY-9033

Re-writer (from source messaging / smart brief to user prompt) for HP
https://jira.corp.adobe.com/browse/FFDY-9101

Work on mixology
https://jira.corp.adobe.com/browse/FFDY-6212

HP image judge
https://jira.corp.adobe.com/browse/FFDY-10074


Mixogy addressing feedback



## Notes from THD
1. who's managing the storage of the re-writer. WE are storing instead of to the GPT because we have images and videos too.
2. We have both the gemini and the GPT-image-2. 

For Steve to crawl the Dell website:
https://adoberesearch.slack.com/archives/C0BD1RQ1RUK/p1786747323008129




## Tesco feedback addressed:
1. We need to get the new Tesco data and train with those. 
2. Bringing in the VLM critique
3. Check distribution, we didn't have enough fries, we'll add more. (ingredient)


Swap not attempted / incomplete [Q1] (6 items)
    regression compared to MR on MVMR.

Reference not extracted correctly
    generation has aspects that are different than reference.
    Could be lighting issue. Specially when there is a huge difference btw ref and scene. 

Unwanted carryover from reference

Original scene elements not cleared

Undercooked / raw appearance

Color washed out / sauce didn't translat

Unnatural plating / convention violated

Fake-looking / merged objects

Eval-set / prompt authoring issues 




**Hooman make it happen: Move to FE HTMLs. 
** Feedback on the stock data for Humain.
** Esthetics P0
** Send latest for NAOU and Mixology to Ajinkya
** How do we make the NAOU scalable beyond the 11 images (gemini + mask). So they might need to adjust the mask a bit. Get this documented. 
** Add examples for the Photo shoot.

**Take the Visa doc of Ana + Print the documents + Put the laptop/monitor on your desk and Attach sticker for desk move


TCCC:
1. The poses and the interactions that they expect in the generated outputs. (or the scenes that they'd like to epxerrtiment on). remove our pose and interaction instructions. 



# Endgoals
## Team
Dong
    1. Add a business impact section to the doc. 
    2. Complte the template the james is sending you. 
    3. Refenrce that this is not a new conversation (it's a ongoing conversation). Talk about the business impact, 
    which is growing (we cannot scale), Either dropping or delaying (which is related to ability to deliver hte product). Also, what does good performance looks like, what are his assigbments today (really clear), and how his completion is going to be measured, outline the measurement (timing, quality) how will this be measured. Do you blieve you can be suscessful in this role? I.e do you blieve that you can meeet my expecations (and not your own).
    Multiple time frames over several weeks, instead of one long frame.
Josh
    1. go over the plan. Make sure Soheil approves
Arpit
    Move everything to the FE HTML viewer. 
    How do we deploy these? 



## THD
MVP
    Use-case development (building in VLM critique as well) so that LLM suggests prompts. 
    end of week contract. Karan. 
    Give the details duration/aspect r/ resolution. 
Model-Data
    Joshua gives plan soheil approves
Re-Writer (+ VLM ciritque)
    Steve gives plan soheil approves
C-Tech work
    1. Tyler to create a 30s-1m minutes fully production ready video. With b-roll stiches
        -ALso short gif like clips that are production ready for a given article. 
    2. Based on this we'll decide what it takes to enable THD to do this themselves.
    3. Where are we with IP gaurdrails

## HP
    Nail-down video requirements
    Document risks (in a ticket and communicate)
    Add VLM cirituqe

## Humain
0. Tech Qual eval
1. L2 Model training
2. Distillation + VLM
3. New VLM critique from Steve
2. Training on new data.
    Get the data released by legal
3. Hooman to document issues with relevance
4. Comparison with other models specially. 
5. Causal clothes and food missions launched
6. Video plan
    **We also need negetive saudi data for video. Videos that are arab but not sasudi.
7. Previous discussions on Humain
    1. Web search grounded captioning. Daniel/Sudeep 
    2. franchisation understanding. Xuhan is doing 
        Qwen 3.5 for captioning , and re-writer.

    3. Vllm judge for the children x-dress. And also pay attention to the captioning. 
    4. We fix it with our critique model. Like the shoes in an image.
    5. Quality is a function of quantity. So we have a lot from outdoors Saudi but not enough from certain buckets. See if we can bake this into the eval. So that for each category we show how much trianing data is available.  
    6. In some prompts Quaraan is not even not even asked. 
    7. Find the religious symbols in the training set. Have a data explorer (embedding based visual search). So we can search for different symbols. 
    8. How many is re-writer issues and how many is the model. 
    9. Visual search for Bindi's in training data.
    10. Pass this to Gemini and see if this looks Saudi (the indian guy drinking tee image).
    11. We need so steretypical images of what a Saudi looks like.
    12. Saudi flag. Web search based re-writing. 
    13. Suadi tradition of touching nose is out of bounds because it's too intimate.



## Tesco
0. From meeting with Prat (08/05)
    Build a proper VLM judge
    see if we can improve with VML critique the onion soup and the brussles that are not charred enough. 
    Maybe we can also do a Dyno based similarity
    Try to feed the ref image several times so that model focuses more on the ref image than the scap.
        Try on the re-writer side to make more abstract. If not we need to train with more abstract caption. 
    See the MR VS MVMR HTML with the masking in both. 

    Repeat the POC with MVMR (the flux might have issues) and later maybe with GPT-2 or nanao banana
    The hand interaction one seems best so far, we should get a more extensive dataset from that.

    Have Matt respond if the background swap that we have is what he expects. 
    
1. See current issues list and fixes
2. Matt to do eval (compare current with MVMR) and suggest whether we fix of work on new use-case. 
3. Needs VLM critic
4. Things we are investigating. Tesco
    1. Additional objects being added from the reference image (like spoon). When it's too integrated in the food.
    2. Masking part, where some of the items in the background were changing. 
    3. Lighting changes which we are addressing (with masking).
    4. Texture issues from the reference when pieces are missing. The baking of the scene images was coming.
    5. The chardness of the brussle sprouts not fully coming through.

## TCCC
1. Finish up talen (Abhinav to pass the last one with body proportions tmw)
2. 3D POC before we give data ask
    **Weifeng should take a 2D from the Sketch Feb and paste on image. Details with Pranav. 
3. NAOU, Mixology














0. Prasana bypassed me, aligned on the requirements from HP with Pranav directly. The result was that he passed in model requirement, instead of API / pipeline requirements. There is certain pre-processing that img4 does 
that we don't have (but can easily add). Then Prasana tried to force manik to do this, leading to a lot of fights
and frustrations on the engineers part. This is why I had to step in. He continued doing this even after the feedback. 

1. We don't handle occlusions (show layer gen, vs pipeline)
2. They were pasting the asset on white background (loosing white pixels)
3. Humain turned off the wrong guardrails. Also push back on verifying the final product. 
1. He also insturcted Pranav so share the results from pieline we are budilng (that's not for this customer)
which confused people. 
4. Zach, i gave feedback on ticket refusal, showed that to ajinkay first, got ambushed at onsite, Wes hupkins didn't even have a call with me about it. Just went straight to zach. 
Also, last time, when I gave feedback on zach giving wrong engineering info, and showing unauthorized things, 
he had sent screenshots to zach.










# chat with Arpit
1. delete all current v2 pipelines. All customer on V3
2. Audit all the existing pipelines (TCCC, THD, Humain, Tesco, HP)
    --Check if these pipelines are connected or seperated? What do they share exactly? 
    --what's the current review/approval process for changing each pipeline. Code ownership. 
    --What's the current smoke test coverage for each pipeline. 
3. Ground truth of Model/Re-writer will remain in Mori/Genie. We will vendor Genie inside of colligo (the same way we do with Mori) so anytime you have a re-writer update in Genie, we just update the version in Colligo.
4.  Versinoning trace. Our models and re-writers have versions (Hareesh to ensure). Every HTML must have these versions in it. The output json from pipeline also has to have the full version. Also the boards plugin file must be directly linked to version (of model and re-writer) beyond just the endpoint URL. We can either put the versions in the plugin file or put the boards in github and make it mandatory to add version in the PR. Or maybe we make model/rewriter version part of the request to the pipeline, so boards will have to send it.
5. During code review we will make sure that Genie never has try/catches (so things don't silently fail). 




# chat with hareesh
1. Plan for the code base. 
2. We're putting everyhing on L2 for tccc
3. Abhinav needs to touch base more closely with Hareesh. Coordinate. 


# THD-video  06/10/2026 (meeting 5)
1. Joshua: Finalize captioning recepe.
2. Steve: Take the cleaning filters from Joshua, do full training on all collected data, and pass the data out to Soheil. 
3. Donsheng: 


# team building event
PGMS first task. During work hours. 

# where should rewirter from hareesh live?
in genie or colligo?

# For the updates:
** Add Vova to the weekly planning meeting.


this is what I did yestserd, this is what I'm doing tomorrow. This is the ticket for what I did.
Hareesh Ravi  [3:05 PM]
updates

---
---
next steps.

---
---
blockers

---

1. Create meeting for eng for DSG, Humain, Tesco, Hp. 

Cancel the every CT/EM one and put our eng. Check with Ajinkya. 

More frequent and ofline updates. But no regular meetings (maybe bi-weekly meetings).


# THD-video  06/08/2026 (meeting 4)
1. BOD scraping from Steve and the indexing/search from Soheil should be done. 
2. Steve to pass 1 or 2 multi shot videos to Joshua for testing. 
3. Run some initial filtering shot segmentation on the data from Steve (Steve to propose a plan)
    We are going to run Qwen for this the goal is to have some data by tomorrow to start captioning.
    Pass the 16 nodes to Joshua. 
4. Joshua to try the examples from 2 with the pipeline with decant (i.e. QA on the shots) + Captions
    The pipeline (from decant) needs to give images too (since we need 10% images)
    The goal is to make sure the final captions are good and also decant does a good job at QA
5. Joshua to provide a draft test set with two columns: Prompts as users would write them (not re-written ones) and reference images (real or generated). + 3 articles to get the conversation started.


# humain video
1. There is a bug on the L2 model. 


# Foundy 4.0 we should try Tesco. 
Prathyusha contribute as point of contact for Tesco. 
Don't do any infra work just be the POC. 


# HP
how are we getting the cables coming out of the devices since the digital twin doesn't have cables in it. 
is it post edit with PS or Instruct Edti with model.

Talk to Zach about prompting guide. 

# get the action items from the re-writer.
Use Tesco and ginipig. 
1. On Friday, each IC shares their weekly plan. We will approve it on 1 hour meeting on Monday.
Then on each day. At 5pm everyone posts an update on what their update is. 

# THD
nano banan with our re-writer and without our re-writer.

Find the first mission ticket. And also look at the tasks Rebecca pointed at.

What's the hack that manuel did to get I2V with Aleph? 
Joshua passed a static video. 
We wanna do I2V and we will use either Apheph or Gen4.5 (runway) whichever is better on I2V.


# talk to Ajinky
1.  Donsheng,
2. What we are building (Daniel stuff)
3. DecantAI

# THD-video  06/03/2026 (meeting 3)
Joshua: Provide comparison of Aleph and gen4.5

# THD-video  06/01/2026 (meeting 2)
Joshua
    Inference results from Aleph and results from Runway 4.5 inference.
    Re-run the training that Soheil ran to understand the pipeline, etc. 

Steve
    1. How much overalp between brightcove and youtube. and color corrected.
    2. Describ3e the format of each of the datasets. Specially find the new (corrected) folder structure for mission data. Consult the THD wiki data section.

Hooman: get started with Steve and Tyler on data collection. 

# THD-video  05/29/2026 (meeting 1)
Soheil blieves product accuracy all comes from the 1st frame, and we should only focus on the physics. 
Joshua: understand code and provide list of ablations on training parameters,etc.
Steve: Produce canvas with over-view of the categories of video-specific data we currently have, accounting of each, and HTML visualization.
Hooman:
1.Get THD L2 data from ASML`
https://jira.corp.adobe.com/browse/FFP-92885
https://adobe.enterprise.slack.com/docs/T024FSURM/F0B70NN3PL5 (canvas)

define use-case and find the exampl.es in this set. 
Add Tyler to this series. 

2. findout if we can scrape youtube. example: https://www.youtube.com/watch?v=DpCA26bvjsY
3. Decant AI for video https://adoberesearch.slack.com/archives/D064J1EAPDZ/p1780090700086009
4. Stock video search: example
[2:45 PM]https://stock.adobe.com/search/video?k=man+trimming+trimmer&search_type=default-asset-click&asset_id=691129520


# humain
more clear error codes on what's rejecting (and logging) for each of the components. On what's rejecting what. 
Deploy 


@hardyh please track these two asks with tickets (and please send me the tickets too so I also track because these are very important).

@ccampbel (or delegates) to deliver IP and NSFW guardrails for THD by June 10th. 
@rsangave to give us final IP guardrails for Humain by June 3rd. You should already have a ticket for this one. Just need to update.

# HP feedback
0. Humans and other objects are sometimes blurry
1. More images looking at the screen (screen can be black)/
2. More age diversity
HS: get back to Dongsheng about elastic preemptible jobs. 


# THD
Look at the trianing data make sure for circular saw , etc we do have examples of correct hand placement. 
We need IP gaurdrails for THD. What's the Estimate. June 17th. A week before this we should give them endpoint.
Find a seed that works well and fix it in the prompt re-writer. And also talk to Mairon see if we can do this.


# Tesco
1. Are the foods they presented final scenes? in their training data? 10k.
2. Is T2I in scope? Like replace the pasta in this image with pizza but without providing the ref image. 
3. The level of control is not the way he is showing in 2.2.2 we are going to take just the image from ref. Keep everything from the seond image and just hullicinate what we had to (like if we had to change the plate to a bowl or something)
4. For the background swap we need to understand the level of editing. 
5. For the comvos (comibining two foods and hullicninating the scene) we need exact requirements. 

**There will be some hullicination of food, how much is a problem? 
**What exactly are the food items? We need a list. 
**Can we scrape their DAM? Is there any more data other than this? 

6. What exactly are the human interactions? Hand reachout and grab food, or pour food, or server food. 
Is it just hands? Or any other human parts? This is a hard use-case. What about Utensiles, Tongues, saucers. 

7.6.1.1 How are we supposed to generate from different angles without ref images ? for the camera angels. 
We definately need a full list of images. So we need to know exactly what the reference images they're gonna give us 
are. Basically, we need a list of priority SKUs. Because we still need to train on ref images. 

Action item for steve: Do food swap with generic multi-ref model from Hareesh, and latest TCCC model and present the results. 




#meeting with Tyler and Michael. Set a use-case reivew. Soheil. 

Talk to Christican on we only do 3 sizes. 





1. Get the generations from Marian. For Rohan.


WE'll use RUnway4.5 for video for THD.
We might need to have an LLM and generate final blog posts for them. TO generate how to articles. 
Connect with Tony on access to this. Get a professional contractor to right CopyWrite material for THD?
June 16 first version, end of June 30th. 


Abhinav Kumar. Ask vova if he can give this guy to us. Aks Ajinkya if someone can help.
Can we have Priti back? 


1. GIve ticket on data analysis to Matthew. 
2. Move the TCCC Meeting for today. Make it earlier.
3. 

** Give usage restrictions doc to Landon.


32 THD and 16 TCCC and 16 HP, 


Tue 11 to 12 all of us. Two hald an our per Lead for c-tech/EM. 
Move meetings to the afternon. 

1-2.


Wed and Thur. 11 to 11:30 standups. in parallel. 

PGM has to create backlog and tickets after every meeting. 



Pranav Aggarwal  [3:50 PM]
There is also some bg fill augmentations we can get done by 3rd party vendor. For that we can use the 32 projections for the skus. @hshariati by when can we get the 32 views of the HP skus? Will plan the data augmentation around that.



HP
1. Which exactly is the OC model that we need to use. 
2. Get it in writing that we are not promising pixel perfect at any stage. THey are saying the future is OC-v2 + 3D digital twins as input. 
3. Hooman create a write up to show our limited commitment.




1. Give some data numbers to Matt. of how much we have. 




** Put together visuals and slides for Humain. 

1. We can onboard humain on eval hub
2. Eval hub doesn't handle conditional logic, change a question before your previous question. Appen has this. We might be able to vibe code this. Sarah Lee.
3. 
Hooman to send ticket for Christian to Hardy to capture all the details of June 1st. SKUs, etc. 
Zach to share details of meeting with customer. 

We have to review the Deck today for TCCC. Hooman to aks Zach. 
what about the dev deploy? 
Make sure Aurelie and Ken have access to TCCC deck. 

Share the compute ask. 
Prepare eval asks. 


**WE should put leyer gen on ASML roardmpa.

## Source of 3D
1. Vendor: Need steps for expediting the 3D vendor with Josh magnetic mobile. As quickly as possible get sample. Hooman to chime in the email thread. (Brandon is the engieern)

Hooman. reach out to Vas. Send email back and ask for Adobe email. Maybe they are approved under a different name.


2. Internal Adobe: There is physical sim, rendering (mateerial properties), and integration.
(made offer to guys), (Wes McDermin)

scale poses with Jan one too. So you can get one pose, but we can get the rest from there. 

*We have quality concerns but might be able to train image model to bridge the gap. 
Question is scale? 
May 11 is cut off for us knowing whether we can count of Jan or not. 

2. 


we;re gonna do a lot of generation. 
We should find a way to submit to append ,etc ourselves for filtering. 

*** We need NSFW for TCCC. 

*** we need to clean up the production pipeline. 
Who's responsible for maintaining the foundry pipeline? 
Can we have seperate pipelines per customer? 


Good point. Yes we will say it. I can also change the prompt to "sitting on a table and showing interest" just to not trigger anyone in the call. It can not be replicated anyways and actually right now the prompt rewriter is not enforcing it properly but I created a Ticket for you guys: https://jira.corp.adobe.com/browse/FFP-86745
@hshariati Pipeline Slide: Can you please provide us such a slide until tomorrow EoD?
Yes I will check with them tomorrow.
(edited)



0. Finish workday tasks.
1. Feedback on Prathusha promp
2. Feedabck on Abhinav. 
    Talk to ajinkya about abhinav pay increase at least. 
3. Email the lawyers. send the form to the bank (scwap) and upload the legal forms.rdf
3. Hareesh and Abhinav need a break. We need to do something for sure. 
5. Process address change. 

1. WE should use the Kate people, instead of Stephanie people because the relevance is not matching Humains. 
2. Use Sudeep agent that goes through all the captions adnd builds re-writer. We also should give the document with all the feedback to claude and have it adjust the captions, maybe pay more attention to length of Thobe etc. 
3. Another thing would be to run a critiq model on our generations to update the re-writer. 
4. Send the 30% cherry picked from the 600 set.



**Relief plan for Hareesh and Abhinav. 


0. Hooman to make sure data is never trained on from general foundry bucket. It has to be moved to customer specific buckets before we can train on. 

Gemini-3.1 pro. 

## Discuss in eng sync
1. Where is video data? for soheil
2. Product / talent bank for TCCC UXP
3. Humain package to be sent out. Also humain eval on humain prompts. 
4. Kanak helping with Steve / adding sketch to the training run. 



## Sync
1. TCCC: eval with updated re-writer, and share early results tmw, have endpoint tmw EOD so they can play with it. 
    By Wed, we can see if we have to update the training, if not work on re-writer. 
    HS to schedule internal readout for Mon 05/4. 32 nodes for training to be done by Thur.

    Data: 1. Stock mission closed today. 
          2. 15k annotated from Kate. Team has received but won't have time to use. 
    
2. THD: Prat did augmentation, we need to caption this data (after verification).
        Thur, we finish TCCC training and start THD. Hopefully, on top of the TCCC. 

        we'll need 4-8 nodes from Wed morning. (2-300k images to caption). And then 16-20 nodes on Thur for trianing. Over the weekend.
        **Steve needs to share total # images and how much it takes per image. So we can estimate. 

        **Pranav / HS might need to do some hand-holding here.

3. Humain: 
        1. Finalize customer requirements (tmw morning)
        2. Understand why our cultural relevance is so different than Humain's
        3. Should we go with IE based?    
        4. We need to add the 8k data from Humain. (Confirm with Kate on timeline)
        4. Data mission briefs to be shared by Camile. No more data gathering till we better understand the requirements. 

4. HP:
        1. We need to run the mask editing + the OC V2 on this. 
        2. We should start training an image model on the 2k data with HP style. 
        
5. Tesco
        1. HS meeting with Matthew tmw to finalize use-case.

6. DSG
        1. Evaluate the work Dong has done and give some suggestions. We might need to find another approach.
        2. Dong is currently working on the mask editing. Waiting for Dong now. 


**Currently evaluating the MR training (by Thu/Fri we'll release the nodes). 




## feedback for Humain
0. We don't know what's the goal? is it culture first, then landmark, then food? Is the most important thing clothing? 
1. Ask humain to send images with issues in email being wrong and being correct. 
2. We got feedback on why people sitting near fire are wearing full Thobes. But this is not on the model to understand, 
you can wear formal clothing in desert (if it's a wedding) or you can wear casula if it's campling. 
3. THere is misalignment between our guidleines and the feedback we received (for exmaple, they complain women have jewlary but in rality they dont).
4. Definately need a list of landmarks. 
5. Text is out of scope. We need to confirm.
6. We wanna go with IE for landmarks. Where are the examples of texts that are not part of the landmark. 

5. How do I get the comments? 


## FOR HS
### Node allocation
1. Every Wed validation the node allocation canvas
2. Make sure all the Jiras are correct on hareesh's canvas. 
3. Once finalized take to the science channel and negotiate. By Wed morning. fd_science_leads
    By Thur morning. fd_science_all
4. On Thur afternoon allocation should be finalized (nodes will move during thur). 


P1 vs P2 (check with Purvak.)


### THD 
THD next steps and feedback and help with Steve
Steve is trying to compete with Prathyusha. He's very good engineer. Does quick things. 
We should have a chat with Vova maybe. 
He shared URLs in the THD wiki page. Make sure he follows the rules. 
He is looking for visibility instead of looking for impact. 
He is not verifying anything / reviewing anything. He does a 100 things but they're not 
the right things. 
https://adoberesearch.slack.com/archives/C0AKWLP0MCY/p1777310605247259?thread_ts=1777309374.350319&cid=C0AKWLP0MCY

The links are open to all Adobe.

Weekly Squad syncs ()
Monday Hareesh/Pranav/Hooman weekly sync. Update eng canvas. (cc Ajinkya)

Hooman work with Steve on THD. 
1. 10min: each should talk about stock mission briefs (who should review what). HS
2. 10min: data augment/eval vendor annotation. HS
3. 10min: weekly goals and todos for each of products. (Hareesh/Pranav)
4. 10min: fires + EM/C-Tech asks. 

Legal review for THD. Ken said. 

Have a better, customer/stakeholder canvas for data people

What external communications exist and how are we streamlining them? 



1. Setup meeting to findout how we are delivering mission data.
2. Get the request sent for our data generation. 
3. Setup conversation with legal. 
4. Review the docs for Tesco, HP, THD, DSG

Hooman to narrow down exactly what the use case is:
    Sync with Matt H. on need to be put in touch with Humain ppl. Keep him in the loop (feed the right info)
Chat with Steve
The Maniken Idea might not keep clothes identity. Also check with Dong about different options. 



 

For Shayan:
1. Fix the genie loop through where the foundry role needs to be used to access foundry data but that role doesn't have access to the rest of the data. Where as the role that has access to the rest of the data doesn't have access to Foundry. Maybe foundry role should have access to everything? 
2. Ingesting mission data right now runs automatically every two weeks. This should also be triggered manaully or as soon as data is available. Also this takes 6 hours to produce a parquet with all the data which then requires us to spend time finding the data out of that parquet. We should get a PQ with just the data we need .
3. Sharing images with Fremes is very problematic. 

Question from Matt: Why are some images approved (that have negative comments in them)?
Is produccing Saudi food actually a fair use-case? 
And then if the landmark accuract is more important than cultural, then we need a different mechanism based on 
Geo tagging. For example, we can have an IE single ref. So when they give a prompt, we'll find the nearest images to that landmark and edit this one. 

HP: Lets see what GW gives right now, then try the same with OC, then try OC + Layer Gen so that we can harmonize. 



1. Get list of cloths we are targetting (1 or 2)
2. Get reference images for the talents in the 6k
3. Get reference images for the actual talent they want to go with. 
4. Dong to generate manikaen images from the 6k images of DSG. Identify which exact model to use. 
5. We'll train a model to take the maniken and reference image of the talent and generate the live shot.
6. Jenniffer to write up the full use-case (from user perspective) and what part Foundry needs to do. 
    Someone needs to write down a commitment for creating the 2D maniken images (from the CG of cloth and CG of Maniken)



Pablo: Thur Noon to hand over the assets for presentation. 
Zach to write up the use-case for HP. 


1. No filter results (add some bad ones)
2. Show full variation capabilities (that re-writer will do) not just time of day.
3. Show the eval numbers definately.
4. Put img5 comparison, Put the real rock too.
5. SHow them the gap btw img5 and current model. And tell them the videos of from very old. and not eve nthe greated, 
and our final will be much better.
6. We had a lot of genAi in the previous one. But we get a lot more rawness. so we should show this side-by-side.
So maybe stephanie can talk about the esthethics. 

Hooman to create DSG infrustructure. 
Hooman to create DSG pluto project.
Hooman to update wiki with this:
https://adoberesearch.slack.com/archives/C0AK1K5DJ0N/p1775847210375379?thread_ts=1775785646.747289&cid=C0AK1K5DJ0N


Can we get two shots of every product. 

Send the canvas of tasks to Hardy


Tue 05/5th 
Wed 05/6th

Use data platform. Hooman. 
Human annotation. Hooman.
Test Gen6 multi-view multi-ref. 
Can they reference by tag and then we pull the image. 



## C-TEch meeting
1. Align with Tyler on videos to make sure they're all feasable
2. Pablo is saying that the marketing materials most suited for business value are the golden hour photos.

**Hs get a time frame commitment for the THD data.

From Ajinkya: reminder to discuss Soheil and foundry-asml requirement canvas etc. with Ajinkya when you meet

Access to Claud with CHarles
Meeting with Humain person for Arpit
Immigration

** Perform analysis to see what data we need for video THD. 
Share Humain HTML with Ajinkya. 
share with Ajinkya. Daily update with Matt/Pablo (and wes).

Be nicer to Tyler/Michael in terms of tone. 


## To ask Hareesh in 1on1
1. Where are we with multi-view multi-ref? 
2. Where are we with our own masked multi-ref? while we wait for Cherry? 
3. Tasks for Soheil?


## THD roadmap with Michal and Tyler
1. Multi-ref + IE
    So Tyler does: Product Swap, Talent swap, object composition (this shirt + this person + ttimmer).
    Get the exact workflows (+ examples) 

2. Share the output of the 3D workflow. 


## Meeting with Substance on HP
1. 9 products that we should put in the background but not pixel perfect. Hs get list from Christian.
2. We also need to get the list of backgrounds. There is 4-5 backgrounds that they're interested in.
3. What is this 0 prompting? 

## 1on1 Ajinkya
1. Zhihao Ouyang
2. Soheil involvment. How to prevent mis-communication. 
    Background pixel pers. 
    Multi-view multi ref
    Multi-Tunr degred
** Hooman to give road map: on internal readouts. For when we need final deployment. **
3. DSG timeline and usecase.
    Ajinkya Kale  [10:22 AM]
        @hshariati lets keep it aligned to the phasing we did with THD ?
    What's Vova involvement here?
2. Video for Humain. + Latency issue
3. Tesco:
    What's Doygu doing here?

Get Niran Amir. on the video. 
Pranav talking to He for Masked stuff.
Make sure we give them the feedback on the data how only 8k is useful and no video. 

Joshua gone April 15th to 27





** Adobe photographers for TCCC shoot. 
8 month for phase 1 ends end of Aug. For humain

ASML has a story telling dataset. Follow up.





1. Do we need Illustraionts? Specially like Birthday and Eid cards, etc. 
2. Do we need an updated list of places. 
3. Follow up with Pablo on where is the data https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3687812013/Cultural+Taxonomy
Are these available? 
4. Where are the 30k from Humain? What's the 8k that they annotated. The 30k is actually just 8k.


## C-tech
Start thread with Miran on Humain data

**It's critical for references and life style shots to be aligned. 
Exact same product. Clean life-style and rif, and multiple views of each.


## From Joshua issues with MR
1. Relative size. We might need padding or a data pipeline to add padding / or aspect ratio
2. New view points. We need multiple references for the same object from different angels. 
3. Interaction with new tool. We need a bunch of data that shows tools being used correctly. Since we cant 
get data for everything, can we have some prior? like interaction points / pose estimation? we could also do this automatically.
4. We should have curriculum learning instead of multi-task. 


## Fix issue
The issues from multip ref (food messed up , etc) can be fixed with the iE. 

1. we don't have neough data. from 120k to 300 total usable. 

Make uxp and boards support multi-ref. 
Narrative: We are gonna have a multi-ref model that works very well for current/old products.
ANd then for new products it'll work with ref. The labels will only come from ref, since the shape 
of all products are the same. Just labels are different. 

**We should point out the issues in the slides (existing products should be very good). new products will have issue.
And we will point these issues out. 


1. Re-upload the data with only 2 seeds for eval hub

## Sync
3. We need to bring multi-ref into Colligo. 
4. Dongsheng to take the captins tonight and give us a re-writer by tomorrow night. 

***
48 nodes ready to go by tomorrow morning. At least 16 by tonight. 
1 GW without tags (multi ref)
1 GW with tags 
1 GR6 without tags.



## TCCC and THD 8GPUs and Humain is 32 GPUs.
Dongsheng to share his plan in Canvas. Be done with re-writer by April 3rd. 



## HP meeting
multiple products might be in the same image. Maximum 4 per image. (laptop, monitor, mouse, keyboard). We need this at some point
not day one but at some point. 




# C-tech/EM sync
## THD
1. Need tyler to evaluate T2I. And then give us an starting prompt set.
2. MM needs model/board access. To start training the customer?
## Humain
We have a ckpt for humain. We need to know how far off the mark we are on the following areas:
technical quality. 
Relevance to Tourism 
Cultural Alignment
H&B
I need @pmunoz to lead 2 an 3. 

Hooman to Sync with Morgan on how involved eval will be. Both Holly and Kate.
We can count on Stephanie and Camilie over longer term. 
We have annotators on our side now.

## TCCC
Need data. 
    We need to see if DAM has what we need or not. Today. 
    Access. Done.
    sending the products. 
    launching mission
## HP
Need to evaluate the data they sent us.
This is just for one product family. 
    How many products?
    Tyler: SKU list and Test set. 
We need to tell THD what to shoot (studio orange).




Product data. Prioratize product data over everything else. Real data. 
If coke says no. Then we need an urgen mission on existing coke products. 

Existing products with multi ref. 
New procusts more images with interaction.
New products 
Ask Rebecca to ask Dom to pus some wieght on it. 


PGM. needs to do this. 

Britany. Kaushal needs to be in the meeting with EM/C-tech




# Xingtai to pass some generated results to MG.
And us to pass the new test set fof the ASML. 


# Thread for every captioning task in the consumer channel. 
1. With the visualizatins (shared by Prathusha) and feedback from the trainers. 
2. Put feedback n Dongsheg thread. 
3. Dongshegk to impelent rewirter idea. sync with Abhinav. 

Hooman to get the color degredation evaluated. 

Likeness for TCCC is not that good. 
We need to remove all the bad logo examples in the synthetic data. 
Hooman to follow up on getting more reference images. 

Sync again when we get the photshoot results. 


--Look at the previous run that Abhinav did without syntehtic data. 



# WE eneed a slack channel with the externals. And schedule metings. 
# Jira. and wiki. Cursor/Claud maybe.




## THD sync
** we're gonna caption everything with GPT and QWen. And we put these in seperate column.
talk to Oliver see if we can turn that off in Azure. 



1. Same engineering sync btwe coke and THD.
2. Seperate engineering sync frm ctech and engagement manangers. 

** Each person that takes a workflow. Needs to do it e2e (data, model, et).

Nominate responsible parties:
1. Arpit: Humain T2I
2. Abhinav: TCCC + THD IE
3. Joshua: General MIR (for THD  + TCCC + others) Prathyusha?
4. Dongsheng: captioning and rewrite for all customers. 
6. Kanak: Sketch (THD)SQ
7. Pranav: maybe do more leadership and the Hareesh to do more on video. 
8. Confirm that we'll have Sudeep. (we won't have him fulltime)

Ajinkya needs to figure something out for Kanak longer term. 

What are we doing with compute management? 


Frontier engineers. 
Hooman to find out what happens when we max out tokens on GPT codex/Claud/Cursor

## Notes with Hareesh
inference parameters. (neg prompt, etc)
data sets (selectin)
captions and formats
re-writer. 
Model. Do the model work just in one customer. 

For captions, we should have agents and we should. 

1. We should always look at the data. Hareesh to share the PR/Jira template workflow. ANd endforce moving forward. 
2. We should understand the problem first. Systematically. IS the RGB values out of range. 
3. Have a cultral alignment meeting. 
4. People thing training is doing things. But in reality before and after is what matters. 
5. Sharing results. HEre are the results here are my observations. Never share results iwthout your observations and next steps. 
6. We need eval metrics. Something like Kizen. We need to bring the autogen back. 





## TCCC
we need to go to higher res. 
Negetive prompt, 
X0. 

Tues 24th of March.


## THD 
kicking off captioning today. And then we can launch the T2I part tomorow. 

--Sketch all of our THD images. Hooman to send tickets to hareesh.
Kanak to share visualizatin of sketch data with hareesh.

--vendor data thta doesn't go through moderatioon.


## TCCC
1. We got the product mapping wrong.

Get the CSV list of the data. in 8k. 



## LG
Alireza to check about diffusion forcing on genProp from KD. 
Add multiple keyframe. 

1. base ckpt ablation from asml
2. data ablation sudeep will try different data recepe
3. adding 1st/last frame. Maybe positioal embedding will help
4. Talk to ratheesh about prompt as input. 

Make sure the timeout is set to not. 

Pull the 4 cardinal direction videos and use as test set.

Lisa is actualyl saying we can do Early April now. 

Nano bananan multi ref on the cardinal directions. Michael to do. 

Edit. 

https://jira.corp.adobe.com/secure/RapidBoard.jspa?rapidView=47160#

sgare data with Xingtai. 

Upsampling is an unknown right now.


## Coke
Santa animated. 

Sunc with Sudeep for the guide for Multi ref
ask them to give us the key frames for the video. 

we saw issue in synthetic data with texts. Kanak regenerated. And also with dimensions.


Add product shots to the brief so we can get the reletive sizes of hands etc when holding the cans. 


## Notes on THD
** res 2k or higher for the mission. Make sure there is at least some 4k. 
** We need multiple ref images form different views. (tool, workpiece, and person).

Need to go to hire res.


1. GR6 MR, with our full THD data? and new trainign parameter. 
    Prathysha. 
* Take a look at SKUS make sure they're good. 
* Eval set from Tyler.

Sudeep will get the instructional in today. Ready actually.

Gloworm can do the image/to sket sketch to image. 



Scap format. Unify the format odf sys prompt for MR captions. 
Proepr eval of GR6 share results with ASML.

--Put the re-writer in prod. 

## Issues with humain ckp
0. Go to scap and make sure gender is added to the sys prompt. 
1. When you caption make sure yo specify all the drinks and make sure none of the can be construed as alcoholic drinks. 
2. Also adding negetive prompts.
3. Make sure the text is handled correctly in inference.

4. Arpit to share sys prompt for new scap as well as some sample captions. 

5. We also need to grab re-writer sys prompt



1. Generate Saudi places with better precision than Nano Bananda.
2. Life-style: 
    traveling, tourisms. 




We are focusing on the toursim. 


Give the 10SKUs 


Realsteate and healthcare are out of scope, Gaming, 3D, too. Sports.
We need to put together a benchmark for this.

** Arabic text generations in the image.
    We need data here. 
** Event and places accuraetely generated
    We need data here.

Brushify has amazing quality landscape. Good vendor. Kaylian mentioned. 

We'll meet again on Thur. 

--GenProp action items:
    1. Start the conversation about Vendor. 

--Talk to Theo team about data transfer. Perfect for him.





### PS action items
1. Talk to Ion about UXP plugin. 
2. Ask Lynn why we have to wait May. Why is this taking 
3. On option is that we just pass the plugin to the markets. 
4. Another way is all their markest have to be on same PS version. 



Maybe reserach/Hareesh can do image to sketch. 


1. GPT is better than Kwen and use the same model for re-write. They used mini. 
2. Dadniel to do a sanity check of our work sys promt, etc.
3. These guys used scap. For t5 should we do 1024. Talk with Sudeep. He also has Qwen for cnditioning. 
Chek which model he has that has Qwen and if we can use that. 
4. Our data is small so we can probably do multiple passes per iamge for captioning. 
5. Daniel to dig up the nalaysis on GPT5 vs mini. 
6. Maybr we should mix the mini and gpt5 to cntrol costs.

6. GPU for IE side is much much better than Qwen. 

7. Daniel to share the code for how they call GPUt.
8. Qwen 3.5 in colligo? Check with Purvak.



### THD data mission
Video or image? Video is the future but we had a lot of issues because our imagary show tools in action. As opposed to in stil shots. Image. 

Our biggest issue is Human orientation. 
We want multi-ref data. They have had issues mixing image and video so our refs might have to come in video.
Can we ask for different tool usage orientations? Like use a drill in different angles and orientations?
    Or the other most common edits that we do. This way we target both our IE and MR use case.
We should also pass the safe usage guides per SKUs. 
Also, we need to finalize our SKUs. Are we sticking to the 10 that we currently have?
They should also provide a text description of what they changed in their pose so we can use during captioning. 

Move away from installation and get closer to the usage. 
We stick to the current 10 SKUs. 

Same tool different poses. And same pose different tools. 


***From Ken: Add more instructions on how many different orientations per tool. We should restrict to a single orientation per tool per contributor. 


For Mid training of GW MR, they need 32 H200.  We can get flash att 4 for B200 (30 of them).
Start the thread. Pair Joshua. 


can Ashwin use their own hardware stuff and pass something to us? instead of Abhinav doing it? 



## TCCC
### Biggest ask mid-March:
    0. talent guide by Wed (the rest are all mid march). Need to reach out. Tue March 24th. In NY. Which includes their Photgrapher. We do March 9th for the internal. 
    1. P0 Acces in PS. 
    2. P0 Degredation fixed. 
    3. P0 Product Likeness
    4. P1 Background edit
    5. We have new list of more food if we are generating assets we should add those too. 


### planned work:
    0. By Tue, Guide for shooting talents. @Hooman. (Rebecca: to get the paired data of raw + color corrected + Rebecca to ask about indentation on bottle missing from training data.)
    1. Make re-write deterministic
    2. evaluate produt likness and background edit
    3. Fix color deg:
        --Run model distillation on 1086k TCCC checkpoint.
            we saw more color consistency. (no CFG, fewer denoising steps)
        --This is all on top of GW GA, 
        --We previsouly saw improvment by neg prompt, and model switcher
        --Adding their small 1000 SF data helped alot, next step is to add our data and see if it works. 
        Also we need to check just simple encode decode to make sure that's not the issue. 

        --Reduced LR -> didn't work
        --Increased BS -> didn't work
        --warm up ?
        --Potentially try EMA?
        --Remove some TCCC data (just T2I didn't help removing IE as well). 
        Is this edit dependant? (comes around edit 3 or 4), (happens in base model around 8 or 9 edits and less degr). For us happens even in 1000 steps. (@hooman: raise ticket to document the details)
        --Potentially try even more of our data (even up to 50%).

        Correcting the previous image before the next edit? 
            compute efficient, but might introduce blending/halo artifacts?

        Should we use 3p model for the edits?
            3p model also has artifacts.

        Adding the coke data hurt the results. But the split got skewed. Abhinav is reducing the split. 

        --Connect with Ashwin. To see if he can ablate and give recpe for distilling in a way that we get quality and not lower timesptes

        --WE use Qwen in rewrite because we had issue with GPU with the characters. We're gonna try this again. we removed talent names because of NSFW as well. 

        --Investigate if instead of just switchng the model we can just call the ff pipeline with our none food edits. 

    4.## PS integration
        1. API similar to IMG5. In prod.
        2. Subscribe to the discovery service AC/CP. We need to push it in for discovery. Thin vu.
            agentic-tooling.entapp.adproto.com (protoshop)
        around May if step 2 works. 
        Ersin needs to talke to Joe

### Unplanned work we have discussed
    0 new model for local edits from Xingtai that Soheil asked to add to our backlog.
    https://huggingface.co/papers/2602.09084

    1. Add the vllm judge. To filter out our training dataset. 
    3. eval the qwen 3. 

    Body parts staying the same or not changing is an issue currently. 
    We're gonna see if this is fixed already, if not, we're gonna 
    add more synthethic data and also give variations in prompt re-write. 

    Adding more synthetic data where we remove people (we deleted this data of adding and removing people)
    We need more data from Coke. 

    add Stock data with food. In the captions we should emphesize on missing food.
    products dimentions need to be added. 

    zack issue with re-write?

    variation of the talent. With more lighting variations. 
    Food proportions: We have some half eaten food in stock data. So maybe this will help.
    Utensiles appear and disappear. Maybe add some changing of chupstic to forks, and utensiles.
    Talent perservation. With the arm being white instead of black (when it's not in the original)

    **Should we also go to 2k?



## LG
### Biggest ask:
    0. Show images and videos that we can do on Wed. We need to finalize these assets immediately. 
        --Images from Lisa and MG. 
        --GenProp data. 
        --V2V data

    1. Mid-March they want to see first footage. 
    2. Internal Deadline is Mid April
    3. External Deadline is first of May

### Planned work
    1. Elie Michelle is trying D4ART (gassian splats)
    2. HenHo is trying their memory v2v (longer context windown)
    3. V2V mdels (Xingtai is trying LTX2 and wan 2.2 vaze). Best for Long/Complex V2V: WAN 2.2 + VACE( Video Aware Crossmodel Encoder) + Context Overlap in ComfyUI allows for generating longer (15s+) videos by using "VACE" to maintain consistency across 5–10 second, overlapping chunks. 
    4. Video Segmentatio models (Arpit found SegmentAnything V2 on Colligo already). He Reached out to @jagan and @mbrack and Scott Cohen who reviewed lot of them recently for layergen/lego.
    5. GenProp. Already saw samples. Gonna get more from Tianyu (Stev) wang using base model.
    6. Check stock for greenery and other relevant data. 



### Notes on customer asks
    --They might want clouds in addition to greeneay, there are some animals that are not in scope probbaly, 
    And there are certain flower types. 
        16bit HDR.
        dry desicated look -> to green.
        Addition of digital Fonda _> learning animals
        Replacing flowers -> with general ones. 
        Window in the train to show the outside night sceneray
        and then also add rain drops to the window.
        Maybe some in-painting. 

        --we can use their Lidar as well as lense test. We can also use camera tracking to get the data from different views. 

### Sync on GenProp
1. Use rendering techniques to get more data.
All curernt data in synthethic. 
They want about 1000 at least 500. 
16. H200 and 16 H100 they have currently.
    Data is their biggest ask not compute. 
They couldn't find any vendor. 
the VFX data for V2V isn't good enough either. The original and vfx are not fully pixel aligned because they used I2V to generate.

Create GneProp channel. 

Ask for more grass, and specific type of flowers. They want specific ones. 

Hooman to talk to Stock. And see if we can hire a VFX artist. 
Talk to Niran on stock side.
Data should focus on Grass.

One issue is that we cannot prompt the GenProp
One issue is multi-key frames.
Send data description to Lisa.

Reconstruct with the VAE on the THD data. To see how bad the VAE is. Do this with the F16 VAE. And try the F32. Alireza.

## THD
### Biggest Asks (Begining of March)
    0. I need to let Stock Mission know by Tue
        6. Mission data probably not ready before end of Q1. (So launch End of Feb) 
        Aurelie Saliba
        Hi @hshariati we can´t accomodate this ask that late in the Q, but we can definitely prepare for it for beginning of Q2. Please prepare a CAREQ with the requirements accordingly. We have committed to several other projects for FF and we follow a very strict scheduling framework: Requirements → Brief Creation → Brief Sign-off → Content Alignment → Production / Missions Launch → BRs → Delivery

    1. Access in Boards
    2. Multi-Ref
    3. Video
    4. THD Summit is April 19th. Internally aim for April 6th. And then an informal one even sooner.


    For data: The biggest issue is the human pose. 


    Let's try captioning with GPT5 think. And rbing in Ajinkya's to verify. Hooman to create meeting. 


    We should try GW with structure caps. Need to confirm if there are token limit. 


### Planned work 
    1. Now that we determined T2I is as good on GW (GA) and GW early ckpt. We should add those SKUs to the GW and drop the IMG5 one.
        issue with trimmer and with ring camera 
    2. We need to eval video and multi-ref when they become available.
        Ultra had issue so they switched to GR6 lite
        share the gpu OOM error. Maybe GPU pinning is wrong. It takes about a day to crash. Wanna make sure we have the same sharding
        as NBCU. 
        We should remove all other validation (just keep ours). TO test run validation after 10 steps to make sure it doesn't crash.
        Hero ablation is better than the Specilist. Both have MR, but Hero has video capability but not 2k. But specialist has 2k t2i and 2k multi ref. 

    3. We need to eval instruct edit. And understand where we are with it. 
    4. Need to productionalize Prompt-Rewrite work that Dongsheng did. With product specific manuals. 
        Dongsheng to share full eval of his re-writer based on menues idea. Then we should see if this benefitst teh training too.
        --Also before re-write was messing with IE. Are these changes just for T2I or for IE too? 

    5. We need sketch/depth/edge to image (Arpit work).

    Abhinav. To deploy to prod the GW ckpt. 
    Waiting on eval of IE from Tyler. 


## Humain

### Biggest Ask (end of Feb)
    1. First Ckpt to evaluate. Internal end of Feb.
    2. LEAP Demo first 2-3 week of March. (LEAP is in April)

### Planned work
    3. Fine tune the first model. 
    4. Figure out the API for the Demo 
        We don't need demo API. Assets are pre-generated.
    5. Run existing prompts (from humain and ff) on IMG5 to see the results.
        Done. Now we need to evaluate this. With Kate
        ff data can't go into either appen nor prolific. But customer data can go in appen. We'll have these in Appen on Friday. 
        Appen has a team that does both English and Arabaic. 
    6. Investigate what changes we need to prompt re-write.
    7. What's the API they need for their demo?
        We need to deploy the ckpt as soon as we have it so Pablo can test and build against.

### Unplanned work 
    1. Evaluation: We have two prompt sets. We will show these to customers. For anything more we need Saudi annotators. We are trting to find out where these come from? 
        We have setup the sseval infra.
    2. Data from Humain has not been useful. What's the plan here moving forward? 
        we need to give them a guide on what kinda data (resolutin etc) is useful for us.

    3. ALAM struggles with the spelling of places and events. For example Maccah can be written in English in many ways.
        We are evaluating against the arabic prompt. 
        If we realize that there are issues we might have a re-writer. (distrbution between arabic and english might be different)
        They also have Alam2.0 so it might be better, can we leverage their eval on that? 



## Foundry Automation
### Data Vis and Packaging
    Can we get a quick strimlit UI where I can search stock, and click a button to get a parquet out of it? 
### Access to data, models, compute
    Proposal from Shayan is almost implemented. 
### Compute Tracking
    Need to learn from Nikita how to do this. Once I can do it as a human, I can automate it. 











## TCCC Readout
Showing the meta data of who's in the generated image. They want this integrated in PhotoShop
It needs to be in a format that people actually use maybe FDI. 

-Specifying wardrobe. And cloths.
-Examples of facial expressions.
-They also have before/after color grading. 
-Layernig is a must to have. And adding to photoshop for retouch later. They really care about being able to select an aread of the image and touch just that part without changing other parts. 
It's less about editing than seeing different options and tuggling through. 

-Their biggest proble is with the color and lighting changing. Specially in talent swap.
-Keeping proportions. Images of full body from models + face expressions + Neutral colors + fitted neutural cloths. + hand shots.

-They're ok with the model not doing more than 4 people. Don't want very busy shots. Maybe we can learn the composition. To have more people but keep the composition. Original Raffa not a big fan of adding people. Maybe we can even constraint the model.

-Guidline for usage and also for how to photograph the talents (Adobe needs to provide).

-Maybe a note on the side pannel should say whether something follows brand guidlines or not. The model shouldn't enforce but it can let the user know. But not there yet. (But this is not as important Raffa says).

-They care about the environment too. Changing the background wall, changing the couch, etc. 

-They don't want it in Boards, they definately want it in Photoshop. 

-They want to see more of the details of Santa. They have big (far) shots of Santa. But they wanna see more details that they haven't seen before. 

-We told them that Santa and the food/talent are same model. They want a roll out in the next few weeks so that they can actually use. 

-How people in different markeets access this? Since their partners have their own photoshop license. Can anyone they give access to in the DAM, have access to their model. Raffa wants anyone with KO acccess to have access to the Foundry model too.

#### Santa Portion
-Being able to have Multi_ref so that they give the reference of the food as well as a style / composition reference.
and then have that food. 








# TCCC 
1. Prompt re-write.
2. Syntehtic data (use the list the rebecca shared.) Use the previous mail campain as reference (to make sure talent is actually eating the food).
3. The videos from stocks. The quaity is pretty similar to coke. We have 57k videos shorts. 
4. Training over the weekend we'll use the SFT dataset from the glowworkm team (with more emphesis on people).
5. More imaged data from St5ocks with people eating food. Talk to Pratheysusha. 


1. Can they also re-direct attention. David to add test cases for this

issues.
2. Plasticy foods, Hullucnation, hands issue. bad color tones, maintaining image composition. 

3. Prompt expansion. (Abhivane)
3. Check if the images look good in train8ing data (or plasticiy).
4. Look at the captiosn (since some of the categories where different). Pepperony pitza didn't exist. 
5. Adding scap to the training. 

5. The portion of the food
6. Glow Worm did ablation on new SFT ckpt. They have speicifc human editing data. 
    Add more syntehtic data.

7. VLLM base instead of T5. (enable). Abhinave take a look.


# THD topics/action items
00. New checkpoint, check the results. Ersin asked to fix hands/etc.
0. Human written test set covering actual narrative/ usecase (ongoing)
    s3://foundry-thd-enterprise-adobe-assets/adobe_evaluation_sets/prompt-benchmark-sets/2026-01-05_024232__single-narrative-smart-locks/

    So the actual prompt entered by the user might be something like:
    "<ACTOR_A> is screwing a phillips head screw into the mounting bracket of <PRODUCT_SKU> using a <TOOL_SKU>. He is on a ladder, working outside the garage of <THD_STUDIO_SET_A>. The lighting soft overcast, but well-lit".

1. We get a list of products and their imagary and train a model to reference products by name. 

2. Caption linearization
3. Text encoding, adding the double tags, and recaptioning. For now we're just going to use the stage. 

4. Join training of image and instruct edit. (Joshua)

5. Glowworm sketch to image.

6. LLM training for prompt re-write.

2. Adding stock data. We have around 160k images. 
5. Re-write prompts in test set
2. Write mission brief on our data gaps
    1.1 final categories + sub-categories (very detailed)
    1.2 how much gap from each category in our training set
    We should launch new mission once training is done (tomorrow) and see how much stock data we have.

    Different kinds of wires coming out of devices. 
    We should ask for more installation videos.
    Devices opened up with wires, etc sticking out. 
    Installing / removing / charging batteries for different smart home devices.
    Screws and screw drivers. Connection between screw and screw driver.

    Smart cameras      	164
    Smart doorbell	198
    Smart Lock	121
    Smart Thermostats	196
    Garage Door Openers	42
    Cordless Drill	8405
    Cordless Blower	437
    Cordless Impact Driver	273
    Cordless Trimmer	866
    Wires	14
    Kitchen	1378
    Bathroom	816
    Switch	73
    Screw	95
    Screw Driver	6
    Rejected

6. Kanauk to do investigation of current training data using captions and give us where the gaps are (how many frames from each categoriy).

4. Multi-Ref (Glowworm) training
    Joshau and Xingtai to connect in Abhinav sync.
    No THD edit data only multi ref data.
    Xingtai is to provide a glimmer module that we can run on THD videos to get multi ref data.
    We will hae to heavily edit this. We'll use this in additon to our 500 images.
    Xingtai to share HTML, branch, config for gabby.
    We also need to sample some edit data using recepe. 
5. Experiment with the cropping of just tool and hand.





# Framework testing
    1. Quick smoke test. Tests the setup, installation, and imports.
    2. E2E glimmer test (throughput, latency)
        2.1 This must use the image caption (vllm based module)
        2.1 This must use the A1 module
    3. E2E training test (through, latency)
        Training config approved by Yuanjun.



## TCCC Action items:
1. Put together a test set (Zack has finished this). Today
2. Put together structure for prompts (Xingtai)
    Add scap to our prompts. Xingtai is doing this today. 50% of

    TCCC has given us a list of names and faces. Xingtai is to augment this with the age category (melenial etc), race, and gender. Because uses will prompt like: melenial-cocasion-male. When there are several matches to this, the model returns
    one at random. 
    Xingtai is to design the captioning system prompt and structure based on this.
    * Prompt rewrite. 

    We have 9k training data. And only 3k have talent food. The rest have nothing to do with food.
    
3. Get food data from stocks. Search for food and people. Hooman.
4. Generate more synthetic data, which costs money. Xingtai to give estimate of how much it'll cost us.
5. Adding scap to the prompts. And deploy for zack. 
6. Hooman to download the data from AEM

4. How do we get data from KO ? This is ersolved. (Hooman)
    Action item on Bchoy to get us the AEM data.
    We have a list of the directories in excepl sheet. Zhack has. We expect about 10k
5. We're gonna get the list of foods and their names. (Rebecca)
6. Coke-products list and their names. (Rebecca)
7. Confirmatin on max number of people in the image. (Rebecca). 1-3 foreground 8-12 in the background.
8. Their do their design summits in march and they want us on main stage. (Feb 1st internal deadline).

* We have less than 50 with Food/Product/People.




## Longer term Action items THD:
*Romania are using img5 but Lora per Layer. They assign a layer per concept. (Ionut)
* Are stuff that Ankeet provided useful? 
* Aubry wants to talk sketch to image.
3. Add shot segment, change system prompt for selection, test on videos
9. adding pose idea. 
10. Adding Lora there is an easier way now. 



# Genie/Glimmer TODO
1. Stephan is investigating how our gen5 removal lead to mem leak. And potential solutions. 
2. Miray is adding some smoke tests on the libs and imports. 
3. We will need recom on some form of performance test that runs a config and monitors mem usage and latency. 



# THD categories
-smart door bells

, Locks, Lights, Thermostats, Garage Door Openers

Handled:
    - Power drills, impact drivers/impact wrenches, cordless caulk gun
    - Chainsaws/hedge trimmers
    - Circular saw/track saw
    - Brad nailer/nail gun
    - Jigsaw/reciprocating saw/Sawzall
    - Miter saw
    - Pole saw
    - Angle grinder
    - Sander/orbital sander
    - Leaf blower
    - Multi-tool




















## Improving genie idea from paul
**The industrty standard for data loading is to use FSX. INstead of partitioning based on buckets.
sensei-fs is FSX (luster is the name for this). The idea is that if we put the index table on FSX, 
it would be faster. You have a bunch of nodes, each downloading the same parqueet from S3. S3 has 
trottling (only a few clients can read at the same time == compute is limited) but with FSX we can 
scale the compute ahead of time to match our load. What is the download strategy currently and how 
much time do we spend on that. The strategy on our current FSX is not good. What meta and openAi do
is that the index table lives on S3. During training, they put the index table on FSX as cache and 
then everyone else reads from this. Setstrype is an fsx operation to distribute the fsx shards along 
the compute. Hooman to find out if it's worthwhile to optimize around this. Genie should be less
dependent on S3. Currently, all we do is S3 pre-partitioning. So being very careful how we name 
the chunks of meta data. S3 assigns 1 compute to one path, but if you have two paths that branch early
and each has a lot of compute, then amazon will give compute to each path. And we told amazon to 
pre-partition for us. So the answer for us is to have our own dedicated FSX so we can add more compute to 
it as needed. The issue is that if our traffic pattern doesn't get use the compute disapears. 
Setup meeting with shayan, paul, Razvan, and Jash Guna.



## why we need Orion
0. Currently, to take a foundry project e2e, you will need glimmer, Genie, colligo, colligo-deploy, Argo CD, Ethos. However, Orion will be a one-stop shop for all of these. Which will make onboarding new people, much easier. 
1. auto scaling (elasticity).
    --similar to existing pluto elastic jobs
2. Entry point of glimmer modules is dependent on artifcatory runtime installs and 
also has access to github, mnt localssd, S3, roles, Pluto specific env variables, etc. Runtime install of glimmer modules is a show stopper for DOD.
    --There are too many glimmer modules and it's simply not feasble for us to fix them all.
    --Glimmer CLI only allows you to run with a single module at a time. Cannot share componenets from different modules (no composability).
3. observability
    --What metrics are here exactly?
    --If I implement a new glimmer module will I get these for free?
    --How to see the metrics/dashboard? 
4. Lineage requirements for features ans assets. (MP has promised this, but we don't know if they fulfill all the requirements by Orion timeline)





## We need to run a pressure test with glimmer
e2e Stress test. 
Send docs on how they can write their own tests ans what the SLA should be for how long their tests can take.
Get PR from Raunak and share with Daniel where they can contribute. 




## Learn
What's the datbase explorer that Miray is using?
Is it DataGrip ? 

## Change the RDS instance type
db.x2iedn.32xlarge

glimmer-postgres

37
Available
Instance
PostgreSQL
us-west-2a
db.r5b.16xlarge

make tickets with SREs. Talk to Razvan, Jie. 


## Talk to James about putting the amazon SQS in glimmer together instead. 
## talk to SOheil about these. 
## talk to Miray remind her 2 relax


# Prathyusha priorities (in order of urgency)


1. New genie table for the unmoderated data
2. Foundry work (the urgent parts)
3. ARB (needs to be done by Wed next week)
4. Ingest the monthly release from ben's team


Ask Miray:
    We should have a seperate Genie table for None moderated data. The ones that have moderation_status false.



Agreement with Naaji:
1. Three labels human moderated, Auto moderated, none moderated. 
2. Can we track the type of the deal (mission, Deal, Stock), Can we surface this in the market place. 



Prathyusha is already helping with Disney. 
Ang is joining as well as another person in SJ. Soheil asked me to keep the company and make them feel at home.
I can collaborate with Ang on Coke. 

Just be very positive but mention that we tried to align with Zhipeng. He kept going back on his written down promises. 
And then he was like lets not align and collaborate at all. 



3. Model Serving (vllm)
4. Dashboard
5. Genie





1. Wiki to show the status of video. Hooman to see who should do it.
https://wiki.corp.adobe.com/display/GenAI/LL+table+release+notes



Oct 8th for Feng.



## VLLM scaling
1. Seperate vllm server vs requst systems gets us 9x improvement. 
2. Higher batck sizes around 100 puts more work on genie but actually helps. Question, model by model how do we decided model servesrr bases on data servers. We should get more metrics to find the bottle neck (idle time and data preprocessing side on Genie/glimmer side). Marion.
3. Compare the same graph (that was generated from glimmer side) with vllm side to make sure we're not overloading the vllm. Maybe Raunak can share the code with Chicu? Biggest concern is running out of resources on the scheduler side. At about concurrncy of 64 waiting requests shoot up.
Understand how many requests are batched together on the vllm side.Raunak. 
Aidtya to share configrts from video sside and example of data job that includes preprocessing to Marion.  


# Discuss with team
Someone needs to look into this. 
https://adoberesearch.slack.com/archives/C08FVJBU3LL/p1754672710848249




Find well defined tasks for Steven and Feng. Not open ended tasks. 1-2 months worth of work. 
E2E model life cycle. And E2E data lifecycle.


## Darshan Prasad
His problem is resources. He has one person that is coming out of PTO. But thinking end of Oct. Needs to talk to hims nanager
Couple of designers in his org too that he'll talk too. Maybe they can give us a design within couple of weeks. 
His ganna talk to his manager to see what they can commit to. 
Suggested we talk to other design teams too.


*Ask peole to contain everything in the channel not DMs
https://adoberesearch.slack.com/archives/C0997L453DM/p1754671969223389


## Steven
1. Townhal presentation. 
Steven to complete the user story and data life cycle. 
2. Feature registry addition
E2E Lineage tracking for data lifecycle (hs to talk to DJ)


## Miray
last mile problem
*** THe PRs are getting out of hand. Look at the canvas Kevin shared. 
Miray to take a look.

Elastic. Working but not out of the box. Changes in the main script are needed. Elastic from CLI
We don't have any dashboard right now. need to talk about this.

## Gopi
1. Prepare an announcement of the work on work bench when the last putting backend errors in frotnend is in.
2. Create run book on how to restart workbench
3. Move the workbench to our own devboxes. (move the ticket to in progress. HS)

## Prythusa
Aspect ratio

## Feng 
vllm final plan.
**Assigning GPUs at random is dangerous. Maybe we should assing evenly.  
## When will we get the vllm deployment plan? need meeting with Feng/Ion
Plan is to wait for profiling from Marion, and then meet Feng/Marian/Ion/Shayan.
 -- measure async performance wtih glimmer/vllms
 When people add many many jobs, it becomes even more difficult to know if jobs are stuck, etc. 
 So we might have to add more observability there. Feng mentioned that Ray offers this. 
    --might be better to have non pre-emptable cpu jobs to batch data to preemptable gpu jobs
    --Feng to look into using Ray.

## Glimmer priorityes
1. Last mile problem
3. Whos allowed elastic? support mix preemptible and none preemptible.
## Can we add some checks quickly to stop the glim stats from getting the aws trottled? avoid gient/frequent queries?
    For glim stat we just told them to not run on watch. Need to take a look if AWS can help.
    Other than this there is a connection problem. Adding some gaurdrails. There might be an upgrade.

## Notes from Market Place demo 1
1. documentation for MP is important put Gopis runbook of backend there.
2. The final demo for externals must have the publish through frontend in it. 
3. Put some guardrails on SQL execution service to avoid bad actors from sending queries that crash backend.


## Hooman
Send job descriptions for backfills
Make sure all customer requests have tickets. Put the tickets in the csv.
Confirm that the CPU jobs will run in Glimmer. Talk to Chicu. Make sure we do this on CPU



## Talk to Miray about last mile problem. Why not use amazon SQS
    Make sure we build what we need in glimmer/gene for elastic now instead of waiting for Pluto to finish. At the very least we need:
    Progress bar, throughput, recoverability/reliablity whats the plan?. How do job priorities work? How do we specify how much resources an elastic job should take. This is glimmer. 

    Talk to Shayan about Pluto runner. (Model serving)
    Need entiryt that brings models up and down, like a JIT server or something elese. 
    This is what 


## Bring up in sync
1. Can we work the slack notification ticket ? request from Adeet.
https://jira.corp.adobe.com/browse/FFP-48912

2. Who can we assign this ticket for trying elastic to?
https://jira.corp.adobe.com/browse/FFP-52062



## requirements for asset identification
1. Uniquness (very small collision rate) P0
2. Fast (under 100ms) id generator (input would be a string). P0
3. We should not allow exact duplicates of data (same video getting different ids)
    This might not be likely when we acquire data. But will be a problem for Keto data.
    Maybe we can have an async dedpu based on MD5sum that we run async. In case, someone
    re-ingests the same keto data twice. 
4. User shouldn't have to load the whole video to get an id generated. P1
5. semantically clips that are from the same video receive similar ids. P2
6. semantically based on an id, user can guess the origin. P2

** Easy way to query the metadata given an ID. 
** S3 bucket permission issue. A dataset might be split in different S3 buckets. 

Issues with using S3 path as id:
    1. Will it solve duplication problem? we do need to propose a solution for this.
    2. What if the path changes? We can build gaurdrails for this.
    3. we can always add the md5 hash as a seperate column. 
        Might not always need to remove all duplicates. 
        Might sometime need to remove near duplicates as well. 

** Who should do the source tagging? Hopefully stock (or added to the self serve identification).
** Dedup algo is still being designed, and is later work.

Issues with loading the whole video:
    1. some videos say in foundry can be 30gb large












## Discuss the issue Baqiao has found:
https://adoberesearch.slack.com/archives/C05521BRZ53/p1754070777085609

## Ticket for the glimmer queue stuff
https://jira.corp.adobe.com/browse/FFP-51323





## what latency gain Feng/Miray see? 
60/70% for Tensorcore utalization.
throughput is not consistenet but average is around 2.5k tokens per second
4GPUs, A100. IVL3 38b. 1S per iteration. And previously 8s per iteration. Image.

Without FSDP 14 iterations/s, 1 ite

**Get a number that we can stand behind.




## Suresh was getting 1.5s-2s on average. But now he gets around 600ms. These are 10s clips. 
    Hugging face + Qwen
    VLLM inference
    VLLM serve
        Feng convern is that when passing images/videos sending over http might be too much. But suresh found out that just base64 images is not problematic.
        Also vllm docs say that for multi gpu, we should use the serve. Their serv helps with more optimized token level parallelization. 

## What is GPU packing and the v3 api with Baqiao ? Get the idea.






Sept 18th and 19th for onside with whole team. 




## SUMMERY meeting with Chicu
1. We should have a pyramid of clips. First at 60s, then 5s, etc
2. NSFW/moderation stuff will run multiple times at different stages. First at movie level, then at clip level
3. Need storage infru? to help with multi level and also with ci/id32 complications.

Data needs to be injested in a format and place that everyone can use it. 

We signed a deal with Moon valey. Their models have a lot of control and they're commercially safe.

If chico can give us an E2E pipeline that delivers the 500M. Then we can learn from it. And build it properly.




## Discuss with Ben


-What's the difference between running queries using Redash vs using workbench? why can't I query the entire training set on the Notebook? 
ATS Cloud (adobe cloud)

**I think we will need all the Redash/GenieWorkbench/Notebook functionality in market place UI. The question is how to do it incrementatlly. 

--At the first step, why can't we just have the backend of the Notebook be in market place backend, so it's one service. 
--Should we also create a palce where they can have dashboards? or somehow just integrate the dashboards created by Redash in the UI?
Showing/displaying dashboards is more important than ability to create/share them. But its good to figure out how to have Redash functionality in MP UI or how to integrate redash directly into it.


Functionality list:
    Self-serve Data Catalog Notebook
        Need Python flexibility to explore ingestion or enrichment data
        Want to share both logic and results in a single notebook
        Prefer in-browser, quick exploration workflows
    Genie Workbench
        Need to run a query a training wide or long table (visit Genie for all features)
    Redash
        Have the goal of eventually creating or contributing to a dashboard


    Basically - Redash is an open-source project we are using to support the Firefly Data Catalog (which is a set of dashboards for ingestion / enrichment data).
    Redash can also be used to write self-serve ingestion queries, but its pretty limited for that use case. Its most useful when you want to create a dashboard and share it.

    Self-Serve Querying –Work with the results of Athena queries either in pandas, or using the %%athena cell magic.
    Ingestion/Enrichment Table Documentation – View table definitions and understand how they fit into the broader data architecture.
    Notebook Sharing with Cell Outputs – Share notebooks containing saved code and outputs for team collaboration.
    Image Visualization Support –Query and visualize image-based datasets directly from your notebook.
    Run Python with Data Science Tooling - PIL, pandas, plotly, matplot, numpy, right in the browser
    Browser-Based Access & Persistence – No compute instance needed; notebooks stored and run entirely in your browser.
    Query Result Sharing via Redash – Generate and share Redash links from Athena queries.



## Todo from Soheil
--Talk to Yuangjun about the data config (yaml) being part of the market place instead of the trainin config.
Generally, data and trainintg code should not be tied together. Learn details from Gopi. 
--Read the docs on data configs and gpu pinning sent by Gopi

--Yuanjun is saying that the Pluto frontend is too slow and he is very concerned about us 
putting the market place UI there natively.
    It's because of ECS

    --Get requirements from Yuanjun for latency of frotnend and pass to Ion.

--Chatbot for support

--Read the parquet management docs from Miray (schedule follow up meeting)


3. Have Gopi walk you through a training config and how it tied to the data config / yaml




## Questions from Soheil 06/20/25
Soheil wants the big table to go to ingestin team. Why?
    Soheil is ok either way
Soheil wants Zhipeng to take over UI for data market place. Why?
    because it needs to integrate to Pluto. + model hub UI, etc. 
    Anything that should always be on should be theirs. 




## From Glimmer workshop 06/20/25
From workshop:
how are credentials managed? are there n docker or ar there from IMS roles
why do people need differnet dockers? why can't everyhting be done through requirements.txt and also the steup.sh



More guidance on how to pick the best group size for the # GPUS and the batch size. 

Performaance is data loader piece and the torch lightning. 
Is the balance between data loader and torch lightning, CPU/GPU computation. Moving tensorrs around.
Maybe we should just hide the group size? 

Generally, we should hide some of the complexity and leave it for adcanced users in a advanced seciton/config. 
Such as group size, docker stuff, etc

We should have a section on what parameters to fine tune for the performance. 

Renditins/writers how things fail silently

No more PR review request on haoran 

Automate the running of glimmer modules. Orchestration. 






# old from ASML times
# record start/end seconds. 
# How to select clips
1. Adobe one audio and video embedding, sort by top similariy to make sure audi/vid aligned.
So dog barking: dog is on the screen ans is barking
2. Audio transcription. Allows us to not cut people off mid senetence. 
3.  Index into it (specially since we have word alingment)
4. Talking head. 

*Audio caption is just not good.

**Py scene detect (shat detection algorihtm) to break down into 60s. 
**Estethics need to run. Clip esthetics. 

***Try to get rid of the 5s limit. 
At least denote based on the middle frame/second and offset from left and right.
Why cant we caption the whole video. 
Can we fit them with an overlap.





## Steps:
1. Get access to the SODA dataset
2. Talk to Prim to understand the data
    What are the meta data: text/captioning, 
    what kinda audio file is it? maybe we run some clarify. 
3. Clipt the long video/audio
    5s audio is not enough we need longer (1min or 50s)
4. Read these in Genie
5. Create a glimmer module
    Tokenize them into tensors


## What Kevin needs:
Pick videos without Narration (only background/ambient) at worse people talking. 
5s chunks
Video caption (with the model we use in prod qwen2.5 7b)
Audo encodings
Code for encoding and decoding audio
50k or so is enough


--Research papers that try to increase temporal consistency or try to make the video do less stuff. Guidance improvmeent 
papers. "Diffusing forcing"
--For the first few generation steps, we fully subtract the predicted noise, but for the rest, we don't. 
Primer: How does T2V work?
    We start from noise. Call this x999
    the model predicts x0 (or what it thinks the x0 was).
    Then we "step" this means we add back noise to x0. This will give us x998
    Then then model again predicts x0. Again we "step", as in, we add noise to the predicted x0
    and we call this x997. All the way, till we no longer add noise. 
    Original latent (B, F, C, H, W)
    [kf,-,-,-,-,-,-,kf,-,-,-,-,-,-,kf] we replicate the original frame (this is I2V)
    At first diffusion step (step 999) the model predicts X0 (or what it thinks is the denoised version)
    [0,999,999,999,999,999,999,0,999,999,999,999,999,999,0]
    So we can keep the original frames (key frames) for a few steps to guide the model towards that. 
    But then later, we drop them (i.e replace them with just the x0 that's predicted.)

--Guided transform when the start and end are very different a lot of stuff happens. We want to smooth than out. 
for example, interpolate the GT latents to create frames in between. And then treat it like a key frame to video. 
--
https://arxiv.org/abs/2407.01392#




4.  JIT using colligo worker (T5, embedding, etc).So similar to t5 componeneet that is used for inference, use that for training as well. [cite: 12]
5.  RAG (beyond just I2V), for T2V. + Pyramidal reviews (low prob of success). [cite: 13]
6

    * JIT using Colligo workers [cite: 18]
    * RAG for T2V [cite: 18]
        * More research [cite: 18]
        * Maybe even Pyramidal reviews (although low prob of success) [cite: 18]




