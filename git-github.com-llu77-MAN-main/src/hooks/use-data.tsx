'use client';
import React, { createContext, useContext, useState, useEffect } from 'react';
import * as initialData from '@/lib/data';
import { format } from 'date-fns';

// Define types for our data
type Employee = typeof initialData.employees[0];
type Branch = typeof initialData.branches[0];
type Product = typeof initialData.productCatalog[0];
type ExpenseCategory = string;
type DailyEntry = {
    branch: string;
    date: Date;
    cash: number;
    network: number;
    employeeSplits: { employeeId: string; amount: number }[];
};
type RecentExpense = typeof initialData.recentExpenses[0];
type ProductOrder = typeof initialData.productOrders[0];
type EmployeeRequest = typeof initialData.employeeRequests[0];
type BonusData = typeof initialData.bonusData[0];

// Define the shape of our context
interface DataContextType {
    employees: Employee[];
    setEmployees: React.Dispatch<React.SetStateAction<Employee[]>>;
    branches: Branch[];
    setBranches: React.Dispatch<React.SetStateAction<Branch[]>>;
    productCatalog: Product[];
    setProductCatalog: React.Dispatch<React.SetStateAction<Product[]>>;
    expenseCategoryList: ExpenseCategory[];
    setExpenseCategoryList: React.Dispatch<React.SetStateAction<ExpenseCategory[]>>;
    dailyEntries: DailyEntry[];
    addDailyEntry: (entry: Omit<DailyEntry, 'date'> & { date: Date }) => void;
    recentExpenses: RecentExpense[];
    addExpense: (expense: Omit<RecentExpense, 'id'>) => void;
    productOrders: ProductOrder[];
    createProductOrder: (order: Omit<ProductOrder, 'orderId' | 'date'>) => void;
    employeeRequests: EmployeeRequest[];
    createRequest: (requestData: any, employee: Employee) => void;
    updateRequestStatus: (requestId: string, action: 'approve' | 'reject', isAdmin?: boolean) => void;
    // Static data that might not change often
    requestTypes: typeof initialData.requestTypes;
    bonusData: BonusData[];
    expenseCategories: typeof initialData.expenseCategories;
    recentTransactions: { id: string, type: string, amount: string, date: string }[];
}

// Create the context
const DataContext = createContext<DataContextType | undefined>(undefined);


const useLocalStorage = <T>(key: string, initialValue: T): [T, React.Dispatch<React.SetStateAction<T>>] => {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') {
      return initialValue;
    }
    try {
      const item = window.localStorage.getItem(key);
      // Important: Handle date parsing for objects that contain dates
      return item ? JSON.parse(item, (key, value) => {
        if (key === 'date' && typeof value === 'string' && value.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z$/)) {
            return new Date(value);
        }
        return value;
      }) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(storedValue));
      }
    } catch (error) {
      console.error(error);
    }
  }, [key, storedValue]);

  return [storedValue, setStoredValue];
};


// Create the provider component
export const DataProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [employees, setEmployees] = useLocalStorage<Employee[]>('employees_data', initialData.employees);
    const [branches, setBranches] = useLocalStorage<Branch[]>('branches_data', initialData.branches);
    const [productCatalog, setProductCatalog] = useLocalStorage<Product[]>('productCatalog_data', initialData.productCatalog);
    const [expenseCategoryList, setExpenseCategoryList] = useLocalStorage<ExpenseCategory[]>('expenseCategoryList_data', initialData.expenseCategoryList);
    const [dailyEntries, setDailyEntries] = useLocalStorage<DailyEntry[]>('dailyEntries_data', initialData.dailyEntries);
    const [recentExpenses, setRecentExpenses] = useLocalStorage<RecentExpense[]>('recentExpenses_data', initialData.recentExpenses);
    const [productOrders, setProductOrders] = useLocalStorage<ProductOrder[]>('productOrders_data', initialData.productOrders);
    const [employeeRequests, setEmployeeRequests] = useLocalStorage<EmployeeRequest[]>('employeeRequests_data', initialData.employeeRequests);
    const [bonusData, setBonusData] = useLocalStorage<BonusData[]>('bonusData_data', initialData.bonusData);
    
    // Combine daily entries and expenses into a unified transaction list
    const recentTransactions = [
        ...dailyEntries.map((entry, i) => ({
            id: `rev-${i}`,
            type: 'إيرادات',
            amount: (entry.cash + entry.network).toFixed(2),
            date: format(new Date(entry.date), 'yyyy-MM-dd'),
        })),
        ...recentExpenses.map((expense, i) => ({
            id: `exp-${i}`,
            type: 'مصروفات',
            amount: expense.amount.toFixed(2),
            date: new Date().toLocaleDateString('en-CA'), // Placeholder date
        }))
    ].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());


    const addDailyEntry = (entry: DailyEntry) => {
        setDailyEntries(prev => [entry, ...prev]);
    };

    const addExpense = (expense: Omit<RecentExpense, 'id'>) => {
        setRecentExpenses(prev => [expense, ...prev]);
    };

    const createProductOrder = (order: Omit<ProductOrder, 'orderId' | 'date'>) => {
        const newOrder: ProductOrder = {
            ...order,
            orderId: `ORD-${String(productOrders.length + 1).padStart(3, '0')}`,
            date: new Date().toLocaleDateString('en-CA'),
        };
        setProductOrders(prev => [newOrder, ...prev]);
    };

    const createRequest = (requestData: any, employee: Employee) => {
        const newRequest: EmployeeRequest = {
            id: `REQ${String(employeeRequests.length + 1).padStart(3, '0')}`,
            employee: employee.name,
            avatar: '',
            type: requestData.requestType,
            date: new Date().toLocaleDateString('en-CA'),
            status: 'قيد انتظار موافقة المشرف',
            details: requestData,
        };
        setEmployeeRequests(prev => [newRequest, ...prev]);
    };

    const updateRequestStatus = (requestId: string, action: 'approve' | 'reject', isAdmin: boolean = false) => {
        setEmployeeRequests(prev =>
            prev.map(req => {
                if (req.id === requestId) {
                    if (action === 'reject') {
                        return { ...req, status: 'مرفوض' };
                    }
                    if (isAdmin) { // Admin's final approval
                        return { ...req, status: 'موافق عليه' };
                    }
                    // Supervisor's approval, moves to admin
                    return { ...req, status: 'قيد انتظار موافقة الأدمن' };
                }
                return req;
            })
        );
    };
    

    const value = {
        employees,
        setEmployees,
        branches,
        setBranches,
        productCatalog,
        setProductCatalog,
        expenseCategoryList,
        setExpenseCategoryList,
        dailyEntries,
        addDailyEntry,
        recentExpenses,
        addExpense,
        productOrders,
        createProductOrder,
        employeeRequests,
        createRequest,
        updateRequestStatus,
        requestTypes: initialData.requestTypes,
        bonusData,
        expenseCategories: initialData.expenseCategories,
        recentTransactions,
    };

    return <DataContext.Provider value={value}>{children}</DataContext.Provider>;
};

// Create a custom hook to use the context
export const useData = () => {
    const context = useContext(DataContext);
    if (context === undefined) {
        throw new Error('useData must be used within a DataProvider');
    }
    return context;
};
