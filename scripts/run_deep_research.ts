import * as fs from 'fs';
import * as path from 'path';
import { executeDeepResearch } from '../src/research/deep_research_service';

/**
 * Main script to run deep research for the Kakuro market
 */
async function main() {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
        console.error("Error: GEMINI_API_KEY environment variable is not set.");
        process.exit(1);
    }

    const requirementsPath = path.join(__dirname, '../research/external_tool_requirements.md');

    try {
        const requirements = fs.readFileSync(requirementsPath, 'utf8');

        console.log("Starting Deep Research for Kakuro market...");
        console.log("This may take several minutes as the agent searches external resources...");

        const result = await executeDeepResearch(requirements, apiKey);

        console.log("\nResearch Completed Successfully!");
        console.log(`Duration: ${result.researchDurationSeconds}s`);
        if (result.tokenUsage) {
            console.log(`Tokens: ${result.tokenUsage.totalTokens} (Est. Cost: $${result.tokenUsage.estimatedCostUsd})`);
        }

        const outputPath = path.join(__dirname, '../research/deep_research_raw_report.md');
        fs.writeFileSync(outputPath, result.rawReport);

        console.log(`\nRaw research report saved to: ${outputPath}`);
        console.log("\nNext step: Parse this report into the respective research/ directories.");

    } catch (error) {
        console.error("An error occurred during research execution:");
        console.error(error);
        process.exit(1);
    }
}

main();
