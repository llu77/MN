'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Wand2, LoaderCircle } from 'lucide-react';
import { getArabicSummary } from './actions';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Separator } from '@/components/ui/separator';

const sampleReport = `For the third quarter of 2023, the barbershop demonstrated strong financial performance. Total revenue increased by 15% to AED 150,000, driven by a 10% rise in service income and a 25% surge in product sales. Net profit saw a significant jump of 20%, reaching AED 45,000. Operating expenses were well-managed, increasing by only 5% despite business growth.`;


export function FinancialReportGenerator() {
  const [report, setReport] = useState(sampleReport);
  const [summary, setSummary] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerate = async () => {
    setIsLoading(true);
    setError(null);
    setSummary('');

    const result = await getArabicSummary(report);

    if (result.error) {
      setError(result.error);
    } else if(result.summary) {
      setSummary(result.summary);
    }
    setIsLoading(false);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>ملخص مالي بالذكاء الاصطناعي</CardTitle>
        <CardDescription>أنشئ ملخصًا عربيًا موجزًا لتقريرك المالي باستخدام الذكاء الاصطناعي.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Textarea
          placeholder="الصق تقريرك المالي هنا..."
          rows={8}
          value={report}
          onChange={(e) => setReport(e.target.value)}
          dir="ltr"
          className="text-left"
        />
        <Button onClick={handleGenerate} disabled={isLoading} className="w-full">
          {isLoading ? (
            <LoaderCircle className="ml-2 h-4 w-4 animate-spin" />
          ) : (
            <Wand2 className="ml-2 h-4 w-4" />
          )}
          إنشاء ملخص بالعربية
        </Button>
      </CardContent>
      {(summary || error || isLoading) && (
        <CardFooter className="flex flex-col items-start gap-4">
            <Separator />
            {isLoading && (
                 <div className="flex items-center space-x-2 text-muted-foreground">
                    <LoaderCircle className="h-4 w-4 animate-spin" />
                    <span>جاري إنشاء الملخص ...</span>
                </div>
            )}
            {error && (
                <Alert variant="destructive">
                    <AlertTitle>خطأ</AlertTitle>
                    <AlertDescription>{error}</AlertDescription>
                </Alert>
            )}
            {summary && (
                <div className="space-y-2 w-full">
                    <h3 className="font-semibold text-right" dir="rtl">ملخص مالي</h3>
                    <p className="text-right text-muted-foreground p-4 bg-muted rounded-md" dir="rtl">
                        {summary}
                    </p>
                </div>
            )}
        </CardFooter>
      )}
    </Card>
  );
}
