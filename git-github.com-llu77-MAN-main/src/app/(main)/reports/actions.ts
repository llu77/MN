'use server';

import {ai} from '@/ai/genkit';
import {z} from 'genkit';


// This flow is now part of the main report generation flow, 
// but we can keep a standalone summary generator for the component on the reports page.

const GenerateArabicSummaryInputSchema = z.object({
  financialReport: z
    .string()
    .describe('The financial report to summarize, in English.'),
});

const GenerateArabicSummaryOutputSchema = z.object({
  arabicSummary: z
    .string()
    .describe('A concise summary of the financial report in Arabic.'),
});

const summaryPrompt = ai.definePrompt({
  name: 'standaloneSummaryPrompt',
  input: {schema: GenerateArabicSummaryInputSchema},
  output: {schema: GenerateArabicSummaryOutputSchema},
  prompt: `You are an expert financial analyst fluent in Arabic.

  Please provide a concise summary in Arabic of the following financial report. The summary should be no more than 3 sentences.

  Financial Report: {{{financialReport}}}`,
});

export async function getArabicSummary(financialReport: string) {
  try {
    const result = await summaryPrompt({ financialReport });
    return { summary: result.output!.arabicSummary, error: null };
  } catch (error) {
    console.error(error);
    return { summary: null, error: 'Failed to generate summary. Please try again.' };
  }
}
