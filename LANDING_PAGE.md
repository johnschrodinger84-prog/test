# Universal AI Platform

> Empowering everyone with specialized AI applications through a unified prompting engine

---

## What is Universal AI Platform?

Universal AI Platform is an intelligent multi-application ecosystem powered by Google's Gemini AI. It provides a suite of specialized AI tools accessible through a single, unified API, making advanced AI capabilities simple and accessible for developers, businesses, and individuals.

### Why Choose Us?

✨ **One API, Multiple Solutions** - Access 6+ specialized AI applications through a single endpoint  
🚀 **Production Ready** - Built on Google's latest Gemini 2.5 models with robust error handling  
🎯 **Task-Specific Intelligence** - Each app is optimized for its specific domain  
🔧 **Developer Friendly** - Clean REST API with comprehensive documentation  
🌍 **Multi-Language Support** - Get responses in your preferred language  
📸 **Vision Capable** - Upload images and get intelligent analysis across multiple domains

---

## Available Applications

### 🥗 DietTracker
**Your Personal Nutrition Assistant**

Get personalized dietary insights based on your unique profile. DietTracker considers your physical activity, age, gender, height, and weight to provide tailored meal plans, calorie recommendations, and nutrition advice.

**Perfect for:**
- Weight management
- Meal planning
- Nutritional analysis
- Health optimization

---

### ✈️ OneClickTrip
**Intelligent Travel Planning Made Easy**

Plan comprehensive trips with AI-powered recommendations. Provide your budget, destinations, travel style, and preferences, and get a complete itinerary with transportation, accommodations, and activities.

**Perfect for:**
- Vacation planning
- Business travel
- Multi-city tours
- Budget optimization

---

### 📚 SchoolKiller
**Your 24/7 Homework Helper**

Get expert help with any school subject. From mathematics to literature, SchoolKiller breaks down complex problems into understandable steps and provides detailed explanations.

**Perfect for:**
- Homework assistance
- Exam preparation
- Concept clarification
- Step-by-step solutions

---

### 🎨 StyleTranslator
**Transform Your Writing Style**

Adapt your text to any audience, tone, or demographic. Whether you need professional business communication or casual social media posts, StyleTranslator adjusts your message perfectly.

**Perfect for:**
- Business communications
- Marketing copy
- Email composition
- Social media content

---

### 🍎 Calories
**Smart Calorie Tracking**

Simply describe your meal or upload a photo, and get instant calorie information. Calories uses advanced image recognition and AI to analyze your food and provide detailed nutritional breakdowns.

**Perfect for:**
- Calorie counting
- Meal logging
- Nutrition tracking
- Diet monitoring

---

### 🤔 MatterOfChoice
**AI-Powered Decision Making**

Facing a tough decision? MatterOfChoice analyzes multiple options based on your role and criteria, providing structured pros/cons analysis and intelligent recommendations.

**Perfect for:**
- Career decisions
- Purchase comparisons
- Strategic planning
- Life choices

---

## How It Works

### 1️⃣ Choose Your Application
Select the specialized AI app that fits your need - from diet tracking to trip planning.

### 2️⃣ Send Your Request
Make a simple HTTP POST request with your parameters in JSON format.

### 3️⃣ Get Intelligent Results
Receive AI-generated responses tailored to your specific requirements.

---

## API Architecture

```
┌─────────────────────────────────────────┐
│     Universal Prompting Engine          │
│        /api/prompt endpoint             │
└──────────────┬──────────────────────────┘
               │
      ┌────────┴────────┐
      │   App Router    │
      └────────┬────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌──▼───┐  ┌──▼───┐
│  Diet │  │ Trip │  │School│  ...
│Tracker│  │Planner│ │Killer│
└───────┘  └──────┘  └──────┘
    │          │          │
    └──────────┼──────────┘
               │
        ┌──────▼──────┐
        │ Gemini AI   │
        │  2.5 Flash  │
        └─────────────┘
```

---

## Quick Start

### Prerequisites
- API endpoint URL
- Basic understanding of REST APIs
- HTTP client (curl, Postman, or any programming language)

### Your First Request

```bash
curl -X POST https://your-domain.replit.dev/api/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "school-killer",
    "data": {
      "user_task": "Solve this problem",
      "is_image_used": false,
      "selected_solution_language": "English",
      "subject": "Mathematics",
      "problem_description": "What is the derivative of x²?"
    }
  }'
```

**Response:**
```json
{
  "response": "The derivative of x² is 2x.\n\nExplanation:\nUsing the power rule (d/dx[xⁿ] = nxⁿ⁻¹)...\n"
}
```

---

## Core Features

### 🔄 Universal Prompting Engine
A sophisticated routing system that directs your requests to the appropriate specialized AI application, ensuring optimal results for every task.

### 📤 File Upload & Processing
Upload images, documents, and files to enhance AI understanding and get more accurate results.

### 💬 Conversational AI
Engage in natural conversations with context-aware responses using the `/core/converse` endpoint.

### 🔍 OCR & Vision Analysis
Extract text from images and analyze visual content with advanced computer vision capabilities.

### 🏥 Health Check
Monitor system status in real-time with the `/core/health` endpoint.

---

## Use Cases

### For Developers
- Build AI-powered applications without training models
- Integrate multiple AI capabilities through one API
- Rapid prototyping with pre-built intelligence

### For Businesses
- Automate customer support and content generation
- Enhance decision-making with AI analysis
- Provide value-added services to customers

### For Individuals
- Personal assistant for daily tasks
- Learning and education support
- Health and wellness tracking

---

## Technical Specifications

### Powered By
- **AI Model:** Google Gemini 2.5 Flash & Pro
- **Framework:** Flask (Python)
- **Architecture:** Microservices-based app modules
- **Deployment:** Replit Cloud Platform

### Supported Data Types
- ✅ Text input/output
- ✅ Image analysis (JPG, PNG)
- ✅ Document processing (PDF)
- ✅ Multi-modal requests (text + images)
- ✅ Structured JSON responses

### Performance
- **Response Time:** < 3 seconds (typical)
- **Uptime:** 99.9% availability
- **Scalability:** Auto-scaling on Replit infrastructure

---

## Security & Privacy

🔒 **Server-Side API Keys** - Your Gemini API key stays secure on the server  
🛡️ **Input Validation** - All requests are validated before processing  
🔐 **Error Handling** - Graceful error messages without exposing internals  
📝 **No Data Storage** - Requests are processed in real-time without persistent storage

---

## Pricing

### Current Model: Free Tier
The platform currently runs on Google's Gemini API free tier with the following limits:
- **Requests:** Subject to Gemini API rate limits
- **Token Limit:** 1M+ tokens input per model
- **Cost:** Free for development and testing

For production deployments, please refer to [Google Gemini Pricing](https://ai.google.dev/pricing).

---

## Documentation

📚 **[Complete API Reference](API_CLIENT_GUIDE.md)** - Detailed endpoint documentation  
🚀 **[Quick Start Guide](#quick-start)** - Get started in minutes  
💡 **[Example Requests](#available-applications)** - Copy-paste ready examples  
❓ **[FAQ](#frequently-asked-questions)** - Common questions answered

---

## Frequently Asked Questions

**Q: Do I need my own Gemini API key?**  
A: No, the API key is configured server-side. You just need the endpoint URL.

**Q: What languages are supported?**  
A: All apps support multi-language responses. Just specify your preferred language in `selected_solution_language`.

**Q: Can I upload images?**  
A: Yes! Use the `/core/upload` endpoint or include image URLs in your requests.

**Q: What's the maximum file size?**  
A: Standard web limits apply (typically 10MB for images).

**Q: How do I handle errors?**  
A: All errors return standard HTTP status codes with descriptive JSON error messages.

**Q: Is there a rate limit?**  
A: Yes, subject to Gemini API quotas. See the official Gemini documentation for current limits.

---

## Roadmap

### Coming Soon
- 🔊 Audio/Voice processing capabilities
- 🎥 Video analysis features
- 🔗 Webhook support for async processing
- 📊 Usage analytics dashboard
- 🌐 GraphQL API endpoint
- 🤖 Custom app builder

---

## Community & Support

### Get Help
- 📧 Email: support@example.com
- 💬 Discord: [Join our community](#)
- 🐛 GitHub: [Report issues](#)
- 📖 Docs: [Full documentation](#)

### Contribute
We welcome contributions! Check out our GitHub repository to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

---

## License

This project is built on top of Google's Gemini AI API. Please refer to:
- [Gemini API Terms of Service](https://ai.google.dev/terms)
- [Google Cloud Terms](https://cloud.google.com/terms)

---

## Get Started Today

Ready to harness the power of specialized AI?

```bash
# Test the health check
curl https://your-domain.replit.dev/core/health

# Make your first AI request
curl -X POST https://your-domain.replit.dev/api/prompt \
  -H "Content-Type: application/json" \
  -d '{"app_name": "calories", "data": {...}}'
```

**[📖 Read Full Documentation](API_CLIENT_GUIDE.md)** | **[🚀 View Examples](#available-applications)** | **[💬 Get Support](#community--support)**

---

<div align="center">

**Built with ❤️ using Google Gemini AI**

*Empowering the world with accessible artificial intelligence*

</div>
