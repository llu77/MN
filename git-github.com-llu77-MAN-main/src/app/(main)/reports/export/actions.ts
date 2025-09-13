'use server';

import { generateFinancialReportWithSummary } from '@/ai/flows/generate-financial-report-summary';
import { recentTransactions } from '@/lib/data';
import { format } from 'date-fns';

interface ReportData {
    reportType: 'revenues' | 'expenses';
    dateRange: {
        from: Date;
        to: Date;
    }
}

export async function generateReport(data: ReportData) {
    try {
        const { reportType, dateRange } = data;
        
        // In a real app, you would fetch this data from your database based on the date range
        // For this demo, we'll filter the mock data
        const financialData = recentTransactions.filter(t => t.type.toLowerCase().startsWith(reportType.slice(0, -1)));

        const result = await generateFinancialReportWithSummary({
            reportType,
            startDate: format(dateRange.from, 'yyyy-MM-dd'),
            endDate: format(dateRange.to, 'yyyy-MM-dd'),
            financialData: JSON.stringify(financialData),
        });

        return { data: result, error: null };
    } catch (error) {
        console.error(error);
        return { data: null, error: 'Failed to generate report. The AI service may be temporarily unavailable.' };
    }
}
