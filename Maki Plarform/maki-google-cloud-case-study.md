# Maki

## Maki reinvents job interviewing at scale with AI and Google Cloud

### Google Cloud results

- Automatic and instant scaling with [Cloud Run](https://cloud.google.com/run)
- Financial and operational optimization using serverless architecture
- Accelerated innovation and deployments with [Vertex AI](https://cloud.google.com/vertex-ai)
- Industrialization of recruitment at scale
- More reliable and bias-free candidate assessments

Maki transforms recruitment by automating interviews using a combination of AI and Google Cloud services. Based on proven scientific methods, the platform conducts real-time interviews, detects cheating, and provides objective scoring on candidate skills.

In a market where applications pour in faster than HR teams can review them, the challenge of recruitment has changed in scale. To help companies hire the talent they truly need, [Maki](https://www.makipeople.com/) imagined a new approach: AI conducting interviews with candidates.

Founded in 2021, the company built its solution on proven scientific methods, drawing notably from Harvard University studies and decades of research in work psychology. These works converge on a single conclusion: structured interviews and multi-measure assessments offer far better predictive capacity than CV analysis or informal chats.

"What allows us to understand a candidate's potential is not their stated background, but the way they reason, adapt, learn, or react in situations close to those they will actually encounter in their professional environment," explains Benjamin Chino, Co-founder and Chief Product Officer of Maki. "Our ambition is to empower companies to accelerate recruitment processes while making assessment more reliable and fair. Thanks to AI, every candidate is measured on the same criteria, according to proven methods, and without the biases that often accompany human interactions. And this applies regardless of volume: A global bank receives nearly 800,000 applications each year but previously processed only a minority due to lack of time. With our platform, they can now assess every applicant, which also means we bring more equity to employment access."

> Our ambition is to empower companies to accelerate recruitment processes while making assessment more reliable and fair. Thanks to AI, every candidate is measured on the same criteria, according to proven methods, and without the biases that often accompany human interactions.
>
> Benjamin Chino
>
> Co-founder and CPO, Maki

## Industrializing scientific assessment with AI

To turn this vision into reality, Maki relied on a combination of AI models and Google Cloud managed services. The heart of the platform rests on a real-time conversational agent capable of conducting the interview, rephrasing a question, or adapting its pace to the candidate's. This voice interaction, developed from open-source models optimized by Maki, is complemented by psychometric models charged with assessing skills: they analyze how a candidate reasons, argues, or solves a problem. At the end of the interview, the platform assigns a score based on the scientific methods that inspired Maki.

To secure interactions and prevent any form of cheating, Maki also uses Gemini Vision to verify that the candidate is alone in front of the screen, identify suspicious behaviors, or detect visual anomalies.

With this sophisticated AI architecture, Maki quickly realized that the quality of its assessments would not be enough to keep the platform's promises: it also needed an infrastructure as solid as it was scalable. This was critical as the platform interfaces directly with clients' ATS (Applicant Tracking Systems), which can lead to massive volumes of applications arriving in a very short time depending on campaigns.

"To conduct our interviews simultaneously and in real-time, we need infrastructure that responds without latency and without volume limits," confirms Benjamin Chino.

Welcome screen for English assessment

"We also needed an environment that allows for fast innovation and simplifies the integration of new models. And that is exactly what we found with Google Cloud: infrastructure that automatically adjusts to the load, favoring cost optimization, and managed services to free us from operational constraints. This allows us to focus our efforts on what truly drives our value added."

> We preferred the serverless approach over a more classic architecture based on Kubernetes because Cloud Run adjusts capacity much more finely, at the level of each request, which guarantees optimal resource adjustment and therefore strengthens cost optimization.
>
> Benjamin Chino
>
> Co-founder and CPO, Maki

## Performance, cost control, and operational simplicity

To build a solution worthy of its ambitions, Maki structured its architecture around Cloud Run and Vertex AI. "We preferred the serverless approach over a more classic architecture based on Kubernetes because Cloud Run adjusts capacity much more finely, at the level of each request, which guarantees optimal resource adjustment and therefore strengthens cost optimization," specifies Benjamin Chino.

Screen showing job applications you can apply for

This elasticity proved decisive during large-scale campaigns, such as when over one million applications had to be processed in less than five days for the recruitment of millions of volunteers for one of the largest sports competitions. "At that time, we didn't yet have an SRE team, and yet the platform remained perfectly stable while our client's infrastructure suffered overload," recalls Benjamin Chino. "Proof that Cloud Run keeps its promises: it adapts instantly, without human supervision, and continues to function where other environments reach their limits."

On the other hand, Vertex AI allows Maki to orchestrate all of its models, whether it be Gemini for automated vision or open-source models.

"Thanks to Vertex AI, we iterate much faster: the platform allows us to test different approaches, compare their performance, and deploy without friction," adds Maki's CPO. Vertex AI also facilitates the deployment of generative AI, which Maki uses primarily internally to accelerate certain processes.

To guarantee data availability, security, and compliance (notably regarding GDPR), Maki also relies on Cloud SQL, while multimedia content generated during interviews (video extracts, visual elements, or audio recordings) is stored in Cloud Storage. Finally, the entire platform is supervised using Cloud Logging and Cloud Monitoring, allowing teams to track performance in real-time, detect potential anomalies, and continuously optimize platform performance.

> Without the reliability and elasticity of Google Cloud services, we could never have grown at this pace. Google Cloud allows us to iterate faster, deploy more serenely, and support very different clients without complicating our architecture. It is a true accelerator for us.
>
> Benjamin Chino
>
> Co-founder and CPO, Maki

## A solid foundation to continue transforming HR practices sustainably

Carried by this solid technological base and the scientific rigor of its assessments, Maki quickly established itself in the market. Available in over forty languages, the platform is now adopted by more than a hundred organizations worldwide.

For a company founded in 2021, this trajectory testifies to the maturity and relevance of its approach, but also to its infrastructure's capacity to support international deployments. "Without the reliability and elasticity of Google Cloud services, we could never have grown at this pace," emphasizes Benjamin Chino. "Google Cloud allows us to iterate faster, deploy more serenely, and support very different clients without complicating our architecture. It is a true accelerator for us."

Office interior with Maki signage in the background

Now solidly established, Maki is already preparing its next evolutions. The enterprise is developing a structured interview module intended for managers to also objectify the final stage of recruitment, and exploring a continuous assessment approach to track skill evolution throughout a professional career. Long term, it envisions further extending its analysis capabilities and proposing new use cases blending vision, conversation, and specialized models.

While the future remains open, one certainty dominates: by combining the finesse of human psychology with the power of Google Cloud services, Maki is not just automating interviews, it is redefining recruitment standards to finally make it as agile as it is fair.

## Summary

Maki relies on Google Cloud and a combination of AI models to automate recruitment interviews and assess candidate skills at scale. By combining scientific methods, real-time conversational agents, and fraud detection using Gemini Vision, the platform offers companies a rapid, objective, and consistent assessment process.

- Industries: Human Resources, Technology
- Location: France
- Products: [Cloud Run](https://cloud.google.com/run), [Vertex AI](https://cloud.google.com/vertex-ai), [Gemini models](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/migrate), [Cloud SQL](https://cloud.google.com/sql), [Cloud Storage](https://cloud.google.com/storage), [Cloud Logging](https://cloud.google.com/logging), [Cloud Monitoring](https://cloud.google.com/monitoring)
