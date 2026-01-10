/**
 * Gemini Deep Research Service for Kakuro Market Analysis
 */

import { GoogleGenAI } from "@google/genai";

const AGENT_NAME = "gemini-2.5-pro"; // Deep Research model

export interface TokenUsage {
    promptTokens: number;
    responseTokens: number;
    totalTokens: number;
    estimatedCostUsd: number;
}

export interface DeepResearchResult {
    status: string;
    rawReport: string;
    researchDurationSeconds: number;
    tokenUsage?: TokenUsage;
}

/**
 * Build the research prompt for Kakuro market analysis based on specific requirements
 */
export function buildKakuroResearchPrompt(requirementsMarkdown: string): string {
    return `Perform comprehensive deep research on the Kakuro puzzle book market for KDP based on the following requirements:

${requirementsMarkdown}

CRITICAL INSTRUCTIONS:
1. Provide SPECIFIC, VERIFIABLE data.
2. For competitors, include actual BSRs, price points, and puzzle counts.
3. For keywords, provide estimated search volumes if available, or at least relative popularity.
4. For pricing, provide a clear recommendation based on current KDP printing costs and competitor ranges.
5. Format the output as a comprehensive markdown report suitable for saving as multiple research documents.

Your response should be structured to address each of the four areas (Competitors, Keywords, Pricing, Trends) in detail.`;
}

/**
 * Estimate token usage and cost
 */
function estimateTokenUsage(prompt: string, response: string): TokenUsage {
    const promptTokens = Math.ceil(prompt.length / 4);
    const responseTokens = Math.ceil(response.length / 4);
    const totalTokens = promptTokens + responseTokens;

    const inputCostPerMillion = 2.00;
    const outputCostPerMillion = 12.00;

    const estimatedCostUsd =
        (promptTokens / 1_000_000) * inputCostPerMillion +
        (responseTokens / 1_000_000) * outputCostPerMillion;

    return {
        promptTokens,
        responseTokens,
        totalTokens,
        estimatedCostUsd: Math.round(estimatedCostUsd * 10000) / 10000
    };
}

/**
 * Main research function
 */
export async function executeDeepResearch(
    requirements: string,
    apiKey: string
): Promise<DeepResearchResult> {
    const startTime = Date.now();
    const prompt = buildKakuroResearchPrompt(requirements);

    try {
        const genai = new GoogleGenAI({ apiKey });

        // Note: Assuming generateContent is the current entry point for the high-level agent
        const model = genai.models.generateContent({
            model: AGENT_NAME,
            contents: prompt,
        });

        const response = await model;
        const rawReport = response.text || "";

        const duration = (Date.now() - startTime) / 1000;
        const tokenUsage = estimateTokenUsage(prompt, rawReport);

        return {
            status: "completed",
            rawReport,
            researchDurationSeconds: duration,
            tokenUsage
        };

    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : "Unknown error";
        console.error(`Research failed: ${errorMessage}`);
        throw error;
    }
}
