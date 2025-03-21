```yaml
---
email: vik@gmail.com
author: Vikas Awasthi
date: 03/20/2025
description: Whether you need to summarize a long document, extract key points, translate content, or transform it into a different format, ContentLens can help.
image: /images/content_lens.jpeg
title:  🔍 ContentLens | AI-Powered Document Insights
categories: ["ContentLens", "AI", "fastHTML", "MonsterUI", "Project"]
---

## Building ContentLens: My Journey Creating an AI-Powered Document Processing App

## Introduction

Over the past weekend, I embarked on an exciting project to build ContentLens - a web application that uses AI to analyze and transform documents. In this blog post, I'll share my experience building this application, the technologies I used, challenges I faced, and what I learned along the way.

## What is ContentLens?

ContentLens is a simple yet powerful application that:
- Accepts various document formats (text, markdown, JSON, DOCX, and images)
- Processes them using Google's Gemini AI
- Returns the results in markdown format that you can download

Whether you need to summarize a long document, extract key points, translate content, or transform it into a different format, ContentLens can help. The application is designed with simplicity and privacy in mind - all uploaded files are processed and immediately deleted.

## The Technology Stack

For this project, I chose to work with:

- **FastHTML and MonsterUI**: These frameworks provided a clean way to build server-rendered interfaces with minimal JavaScript
- **Python**: As the backend language, handling file processing and API integration
- **Google Gemini API**: For the AI capabilities that power the document analysis
- **Railway**: For deployment and hosting

## Building the Application: Step by Step

### 1. Planning the Architecture

I began by planning a clean object-oriented architecture with these main components:
- Document class for handling different file types
- Processor class for interacting with the Gemini API
- Web routes for handling user requests

### 2. File Processing Challenges

One of the more challenging aspects was handling different file types. Each format required a different approach:
- Text and markdown files needed simple reading
- DOCX files required parsing with python-docx
- Images needed special handling for the AI

I implemented a strategy pattern where the Document class would handle extraction differently based on file type.

### 3. Privacy and Security Considerations

From the beginning, I wanted to ensure user privacy. I implemented:
- Immediate deletion of uploaded files after processing
- Removal of processed results after download
- Environment variables for API keys
- Input validation and error handling

### 4. User Experience Enhancements

Based on feedback from early testers, I added:
- File upload indicators
- Processing status feedback
- Dark mode compatibility
- Helpful example instructions

## Lessons Learned

This project taught me several valuable lessons:

1. **The power of separation of concerns**: By keeping document handling, AI processing, and web interfaces separate, the code remained clean and maintainable.

2. **The importance of user feedback**: Adding visual indicators for uploads and processing made the application much more user-friendly.

3. **Deployment considerations**: Ensuring environment variables were properly set up in Railway and that file paths worked correctly in the deployed environment.

4. **The value of iterative development**: Starting with a minimal viable product and adding features based on feedback proved effective.

## Future Enhancements

While ContentLens is functional, there are several enhancements I'm considering:

- Support for more file formats (PDF, EPUB)
- Batch processing of multiple files
- Custom AI model selection
- User accounts for saving processing history
- Additional output formats beyond markdown

## Try It Out!

You can try ContentLens yourself at [contentlens-production.up.railway.app](https://contentlens-production.up.railway.app) or check out the code on [GitHub](https://github.com/vikasAWA/contentlens).

I welcome any feedback or suggestions for improvement!

## Conclusion

Building ContentLens was both challenging and rewarding. It allowed me to combine my interests in web development and AI while creating something practical that others can use. The project demonstrates how powerful modern AI APIs can be when integrated into even relatively simple applications.

What started as a weekend project has turned into something I'm proud to share with others. I hope you find it useful, and I look forward to continuing to improve it based on user feedback.


*Have you tried ContentLens? What document processing features would you find most useful? Let me know in the comments!*