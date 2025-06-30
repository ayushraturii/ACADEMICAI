# An Academic Chatbot Assitant For Btech Cse Scholars

## Motivation
Lot of students struggle to gather notes and read those long long materials during exam nights .It takes a lot of effort and hustle to gather notes ,PYQ's during semester exams.
To overcome this hassle i develop this chatbot assistant which helps Graudates to Score and learn the concepts easily. 

## Insight 
- This project is implemented using Langchain for developing the Ai component.For backend we use FastAPI and for frontend we use HTML,CSS and Javascript. In Future it is planned to go with React to make it morescalable

## Working
Before breaking down each component i believe its good to go first with the working principle.How project is working and what flow or path it is following.

``` 
UI (user sends query)-->FastAPI (sends query ) --> RAG Retrive context from vectorstore
                                               --> LLM combine query,context and history
    --> Sends the response to fastapi --> Append the response to UI

    (I will paste a well diagram later)
```

# Component building
- Lets begin with developing how i thought process this project.The heart of this project is RAG so i develop it first

## RAG
- To build RAG i gathered all the pdfs of notes and pyq's and store them in a directory
- Then with the help of DirectoryLoader and PypdfLoader I Load the pdf into memory.
- since it is hard to make a page a vector i split it into chunks. For text splitting i used Recurisivetextsplitter where we use chunnk size of 2000 and overlapsize of 200 due to memory constraint (Usually chunk size of 1000 is prefer but my system lags for now. In future we can go with a large or cloud native vectordatabase to overcome this.(PineCone))
- Now we have well Documented chunks its time to put them in vectorstore in form of vectors
For this i previosly use Chroma but its not suitable for large vectors So I shift to FAISS
for embedding function i use Google's embedding model. and save the model on disk.
- So far we have Develop our vector database now its time to implement a retriveal component
- I use Vectore.as_retriver() which is basic . I tried to implement a Multiquery_retriver but it causing error so i discard it later we will figure out how we can implement a better retriver because it is one of the main component.

## LLM 
Now we combine this the retrived context to LLM and return the response.we had used Google gemini model for LLm implementation

## Prompt
- for now i just add a basic prompt but later we will figure out a efficient prompt beacause Prompt has a lot of potential.

## BACKEND
- For Backend i develop A FASTApi for scalable query and also i recently studied so i had to implement it (As i heard FastAPI is industry graded but you can go with Flask)
- It is very basic with some validation ,history is maintained here and then it sends the query to LLm with history,context and query.

## Frontend UI
A basic html ,css javascript code to give a feel like a chatbot.

## WHAT NEXT
- Now so far i had developed this project and its working quiet impressive but there are lot of practices what i need to fix but thats future scope for now the current good to go thing is that i want to figure out some way to deploy this.
- If you are reading this and have a idea of how can i deploy this other than the ways i am writing below and is as easy please contact me
* we can try vercel kind of platform
* can dockerize this and then push the container on ec2 (i recently learn so chances are higher i will go with this.)

### what changes i will initiate as soon as possible
* ADD more notes pdf 
* implementing unstructured pdf loader for images and scanned pdf
- semantic based text splitter (its experimental can be seen later not now) or chunksize could be reduced to 1000
* Can shift to cloud vector store pinecone would be great but size might be a issue there
* A good retriver chain could be used
* A prompt that leverages best result like (we could add instructoon to summarize ,tell me like a 5yr old ,simplify the explanations ,use examples ,maintain academic tone)
* In FASTApi we could figure some more validation part
* For frontend we can opt for REACT as it will me more scalable and looks more practical for such project although current scripts are also working fine


