import os
import google.generativeai as genai
from application.config import local_data_path

class SummarizerAI:

    def __init__(self, model_name = "gemini-1.5-flash", max_output_tokens = 10_000):
        self.model = genai.GenerativeModel(
            model_name = model_name,
            generation_config = {
                "temperature" : 1,
                "top_p" : 0.95,
                "top_k" : 64,
                "max_output_tokens" : max_output_tokens,
                "response_mime_type" : "text/plain"
            },
            
        system_instruction = 
        '''
            You are an GEN AI Video summarizer. User will upload a pdf file containing the transcript of the speaker of the video lecture.
            The pdf file would also contain some images or links for reference. You have to summarize the video lecture using the transcript
            in a proper format. You have to summarize the video lecture in such a way that the user can understand the video lecture without
            watching the video. Use proper structure of headings and bullet points for the summary and include every point of the lecture.
            Ensure proper grammar and punctuation in the summary and porper markdown syntax for the headings and bullet points.
        '''
    )

    prompt_message = "Summarize the video using this transript."

    def getGeneratedSummary(self, transcript_file_uri_list):
        uploaded_transcript_files = []
        
        # Fetch and upload the transcript files to the Gemini Server
        for transcipt_file_uri in transcript_file_uri_list:
            uploaded_transcript_files.append(genai.upload_file(
                path = os.path.join(local_data_path, transcipt_file_uri[0]),
                mime_type = "application/pdf"
            ))     

        summary_list = []
        
        # Fetch and store the generated summary
        for uploaded_transcript_file in uploaded_transcript_files:
            summary_list.append(self.model.generate_content([
                self.prompt_message,
                uploaded_transcript_file
            ]).text)
            
            # Delete the uploaded file
            uploaded_transcript_file.delete()
                
        return summary_list
    
class ProgrammingAssistantAI:

    def __init__(self, model_name = "gemini-1.5-flash", max_output_tokens = 1_00_000):
        self.model = genai.GenerativeModel(
            model_name = model_name,
            generation_config = {
                "temperature" : 1,
                "top_p" : 0.95,
                "top_k" : 64,
                "max_output_tokens" : max_output_tokens,
                "response_mime_type" : "text/plain"
            },
            
        system_instruction = 
        '''
            You are an GEN AI Programming Assistant. User will provide you a
            problem statement of a programming problem. The user may ask you to
            provide hints, if you user asks for the hints, then you just provide
            indirect hints such that the user can solve the problem on his/her,
            please don't provide the direct solution. If the user asks to check
            the code it provides, then you can provide the feedback on the code
            and suggest the changes if needed, but don't provide the direct code.
            If the user asks to review the code, then you analyze the code provided
            by the user and provide the feedback on the code and and any better
            solution or approach to solve the problem.
        '''
    )
        
    def getHitsForProblem(self, problem_statement):
        user_prompt = "Hello consider this problem statement: "
        + problem_statement
        + "\n\n Could you provide the hints so that I can solve the problem on my own?"

        response = genai.generate_text(user_prompt)
        return response.text
    
    def getHintsForCode(self, problem_statement, code):
        user_prompt = "Hello consider this problem statement: "
        + problem_statement
        + "\n\n Could you provide the hints so that I resolve the errors in the code on my own. "
        + "Here is the code that I have written on my own: \n\n"
        + code

        response = genai.generate_text(user_prompt)
        return response.text
    
    def getAlternateSolution(self, problem_statement, code):
        user_prompt = "Hello consider this problem statement: "
        + problem_statement
        + "\n\n Could you provide the alternate solution to the problem. "
        + "The code I wrote is correct and works but I want to see if there is any better solution. "
        + "Here is the code that I have written on my own: \n\n"
        + code

        response = genai.generate_text(user_prompt)
        return response.text