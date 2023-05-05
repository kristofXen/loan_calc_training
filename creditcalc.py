import math
import argparse
import sys


class DiffLoan:
    def __init__(self, principal, interest, nr_of_payments):
        self.principal = principal
        self.interest = interest/100/12
        self.nr_of_monthly_payment = nr_of_payments
        self.total_amount_paid = None

    def calc_mth_diff_payment(self, current_month):
        c1 = self.principal-(self.principal*(current_month-1))/self.nr_of_monthly_payment
        dm = self.principal/self.nr_of_monthly_payment + self.interest * c1
        return dm

    def calc_monthly_payment(self):
        total_amount_paid = 0
        msg = ''
        for i in range(1, self.nr_of_monthly_payment+1):
            dm = math.ceil(self.calc_mth_diff_payment(i))
            total_amount_paid = total_amount_paid + dm
            msg = msg + 'Month ' + str(i) + 'payment is ' + str(dm) + '\n'
        self.total_amount_paid = total_amount_paid
        return msg

    def calc_overpayment(self):
        return self.total_amount_paid - self.principal


class Loan:

    def __init__(self, interest_per_month: float = None):
        self.interest: float = None
        self.calc_interest(interest_per_month)

        self.principal: float = None
        self.nr_of_monthly_payment: int = None
        self.monthly_payment: float = None  # annuity
        self.last_payment: float = None

    def calc_interest(self, interest_per_month):
        self.interest = interest_per_month/100/12

    def calc_nr_of_monthly_payment(self,
                                   principal: float,
                                   monthly_payment: float):
        self.principal = principal
        self.monthly_payment = monthly_payment
        x = self.monthly_payment/(self.monthly_payment - self.interest * self.principal)
        period = math.log(x, 1 + self.interest)
        self.nr_of_monthly_payment = math.ceil(period)
        self.calc_last_payment()
        years = math.floor(self.nr_of_monthly_payment/12)
        months = self.nr_of_monthly_payment - years*12
        if years < 1:
            if months == 1:
                msg = 'It will take 1 month to repay this loan!'
            else:
                msg = 'It will take ' + str( months) + ' to repay this loan!'
        elif years == 1:
            if months == 0:
                msg = 'It will take 1 year to repay this loan!'
            elif months == 1:
                msg = 'It will take 1 year and 1 month to repay this loan!'
            else:
                msg = 'It will take 1 year and ' + str(months) + ' months to repay this loan!'
        else:
            if months == 0:
                msg = 'It will take ' + str(years) + ' years to repay this loan!'
            elif months == 1:
                msg = 'It will take ' + str(years) + ' years and 1 month to repay this loan!'
            else:
                msg = 'It will take ' + str(years) + ' years and ' + str(months) + ' months to repay this loan!'
        return msg

    def calc_monthly_payment(self,
                             principal: float,
                             nr_of_monthly_payments: int):
        self.principal = principal
        self.nr_of_monthly_payment = nr_of_monthly_payments

        n = self.interest * (1 + self.interest)**self.nr_of_monthly_payment
        d = (1 + self.interest)**self.nr_of_monthly_payment - 1
        a = self.principal*(n/d)
        self.monthly_payment = math.ceil(a)
        self.calc_last_payment()
        if self.monthly_payment == self.last_payment:
            msg = 'Your monthly payment = ' + str(self.monthly_payment) + '!'
        else:
            msg = 'Your monthly payment = ' + str(self.monthly_payment) \
                   + ' and the last payment = ' + str(self.last_payment)
        return msg

    def calc_principal(self,
                       monthly_payment: float,
                       nr_of_monthly_payment: int):
        self.monthly_payment = monthly_payment
        self.nr_of_monthly_payment = nr_of_monthly_payment

        n = self.interest * (1 + self.interest) ** self.nr_of_monthly_payment
        d = (1 + self.interest) ** self.nr_of_monthly_payment - 1
        p = self.monthly_payment / (n / d)
        self.principal = math.ceil(p)
        self.calc_last_payment()
        msg = 'Your loan principal = ' + str(self.principal) + '!'
        return msg

    def calc_last_payment(self):
        self.last_payment = int(self.principal
                                - (self.nr_of_monthly_payment - 1) * self.monthly_payment)
        self.last_payment = self.monthly_payment
        return self.last_payment

    def calc_overpayment(self):
        return (self.monthly_payment * (self.nr_of_monthly_payment-1) + self.last_payment) - self.principal


# def old_main():
#     print('Enter the loan principal:')
#     principal = float(input())
#
#     loan = Loan(principal=principal)
#
#     print('What do you want to calculate?')
#     print('type "m" for number of monthly payments,')
#     print('type "p" for the monthly payment:')
#
#     m_or_p = input()
#
#     if m_or_p == 'm':
#         print('Enter the monthly payment:')
#         amount = float(input())
#         loan.set_monthly_payment(amount)
#
#         if loan.nr_of_monthly_payment == 1:
#             print('It will take 1 month to repay the loan')
#         else:
#             print('It will take ' + str(loan.nr_of_monthly_payment)
#                   + ' months to repay the loan')
#
#     elif m_or_p == 'p':
#         print('Enter the number of months:')
#         period = int(input())
#         loan.set_nr_of_monthly_payment(period)
#
#         if loan.last_payment == loan.monthly_payment:
#             print('Your monthly payment = ' + str(loan.monthly_payment))
#         else:
#             print('Your monthly payment = ' + str(loan.monthly_payment)
#                   + ' and the last payment = ' + str(loan.last_payment))
#
#     else:
#         print('not-impl')

def annuity(p, a, n, i):
    pd = dict()
    pd['p'] = dict(var='principal', msg='Enter the loan principal:', value=p)
    pd['a'] = dict(var='monthly_payment', msg='Enter the monthly payment:', value=a)
    pd['n'] = dict(var='nr_of_monthly_payments', msg='Enter the number of periods:', value=n)
    pd['i'] = dict(var='interest', msg='Enter the loan interest:', value=i)


    loan = Loan(interest_per_month=pd['i']['value'])
    for k, v in pd.items():
        if v['value'] is None:
            if k == 'p':
                msg = loan.calc_principal(monthly_payment=pd['a']['value'],
                                          nr_of_monthly_payment=pd['n']['value'])
            elif k == 'a':
                msg = loan.calc_monthly_payment(principal=pd['p']['value'],
                                                nr_of_monthly_payments=pd['n']['value'])
            elif k == 'n':
                msg = loan.calc_nr_of_monthly_payment(principal=pd['p']['value'],
                                                      monthly_payment=pd['a']['value'])

            else:
                print('notimpl')

    print(msg)
    print('Overpayment = ' + str(loan.calc_overpayment()))


def diff(p, n, i):
    loan = DiffLoan(principal=p, nr_of_payments=n, interest=i)
    msg = loan.calc_monthly_payment()
    print(msg)
    print('Overpayment = '+str(loan.calc_overpayment()))


def run_main(args):
    if args.type == 'annuity':
        annuity(p=args.principal, a=args.payment, n=args.periods, i=args.interest)
    else:
        diff(p=args.principal, n=args.periods, i=args.interest)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type')
    parser.add_argument('-n', '--periods', type=int)
    parser.add_argument('-p', '--principal', type=float)
    parser.add_argument('-i', '--interest', type=float)
    parser.add_argument('-a', '--payment', type=float)

    args = parser.parse_args()

    if args.type == 'diff' or args.type == 'annuity':
        pass
    else:
        print('Incorrect parameters')
        sys.exit(0)

    if args.type == 'diff' and args.payment is not None:
        print('Incorrect parameters')
        sys.exit(0)

    if args.type == 'annuity':
        if len(vars(args)) < 4:
            print('Incorrect parameters')
            sys.exit(0)

    if args.interest is None:
        print('Incorrect parameters')
        sys.exit(0)

    for k, v in vars(args).items():
        if isinstance(v, float):
            if v < 0:
                print('Incorrect Parameters')
                sys.exit(0)

    run_main(args)
