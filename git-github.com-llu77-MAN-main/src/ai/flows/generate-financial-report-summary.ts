// This file is machine-generated - edit at your own risk!

'use server';

/**
 * @fileOverview Generates a financial report with an AI-generated Arabic summary.
 *
 * - generateFinancialReportWithSummary - A function that generates the financial report and summary.
 * - GenerateFinancialReportWithSummaryInput - The input type for the generateFinancialReportWithSummary function.
 * - GenerateFinancialReportWithSummaryOutput - The return type for the generateFinancialReportWithSummary function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const GenerateFinancialReportWithSummaryInputSchema = z.object({
  reportType: z.enum(['revenues', 'expenses']).describe('The type of financial report to generate (revenues or expenses).'),
  startDate: z.string().describe('The start date for the report period (YYYY-MM-DD).'),
  endDate: z.string().describe('The end date for the report period (YYYY-MM-DD).'),
  financialData: z.string().describe('The financial data in JSON format to be included in the report.'),
});
export type GenerateFinancialReportWithSummaryInput = z.infer<
  typeof GenerateFinancialReportWithSummaryInputSchema
>;

const GenerateFinancialReportWithSummaryOutputSchema = z.object({
  report: z.string().describe('The generated financial report in printable format (e.g., HTML or Markdown content).'),
  arabicSummary: z.string().describe('A concise summary of the financial report in Arabic.'),
});
export type GenerateFinancialReportWithSummaryOutput = z.infer<
  typeof GenerateFinancialReportWithSummaryOutputSchema
>;

export async function generateFinancialReportWithSummary(
  input: GenerateFinancialReportWithSummaryInput
): Promise<GenerateFinancialReportWithSummaryOutput> {
  return generateFinancialReportWithSummaryFlow(input);
}


const reportGenPrompt = ai.definePrompt({
    name: 'reportGenPrompt',
    input: { schema: GenerateFinancialReportWithSummaryInputSchema },
    prompt: `You are a financial analyst. Generate a professional financial report based on the following data.
    The report should be in English and formatted as simple HTML. Include a title, the date range, and a summary of the data.
    
    Report Type: {{{reportType}}}
    Start Date: {{{startDate}}}
    End Date: {{{endDate}}}
    
    Financial Data (JSON):
    \`\`\`json
    {{{financialData}}}
    \`\`\`
    
    Begin the report now.`
});

const summaryPrompt = ai.definePrompt({
    name: 'summaryPrompt',
    input: { schema: z.object({ englishReport: z.string() }) },
    output: { schema: z.object({ arabicSummary: z.string().describe('A concise summary of the financial report in Arabic.') }) },
    prompt: `You are an expert financial analyst fluent in Arabic.

    Please provide a concise summary in Arabic of the following financial report. The summary should be no more than 3 sentences.
    
    Financial Report: {{{englishReport}}}`
});


const generateFinancialReportWithSummaryFlow = ai.defineFlow(
  {
    name: 'generateFinancialReportWithSummaryFlow',
    inputSchema: GenerateFinancialReportWithSummaryInputSchema,
    outputSchema: GenerateFinancialReportWithSummaryOutputSchema,
  },
  async input => {
    // 1. Generate the full English report
    const reportResponse = await reportGenPrompt(input);
    const englishReport = reportResponse.text;

    // 2. Generate the Arabic summary from the English report
    const summaryResponse = await summaryPrompt({ englishReport });
    const arabicSummary = summaryResponse.output!.arabicSummary;

    return {
      report: englishReport,
      arabicSummary: arabicSummary,
    };
  }
);
