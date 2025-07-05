from tkinter import *
from tkinter import messagebox, ttk
import random, os, tempfile, smtplib
import datetime
from database import BillingDatabase  # Import our database module

# Initialize the database
db = BillingDatabase()

# Global variables
billnumber = random.randint(500, 1000)
PRODUCT_PRICES = {
    "Bath Soap": 20, "Face Cream": 50, "Face Wash": 100, "Hair Spray": 150, 
    "Hair Gel": 80, "Body Lotion": 60, "Rice": 30, "Daal": 100, "Oil": 120,
    "Sugar": 50, "Tea": 140, "Wheat": 80, "Maaza": 50, "Frooti": 20,
    "Pepsi": 20, "Coco Cola": 90, "Dew": 30, "Sprite": 45
}
TAX_RATES = {"cosmetic": 0.12, "grocery": 0.05, "drinks": 0.08}

#functionality Part
def clear():
    """Clear all entry fields and reset to default values."""
    entries = [
        bathsoapEntry, facewashEntry, facecreamEntry, bodylotionEntry,
        hairgelEntry, hairsprayEntry, daalEntry, wheatEntry, riceEntry,
        oilEntry, sugarEntry, teaEntry, cococolaEntry, pepsiEntry,
        dewEntry, maazaEntry, frootiEntry, spriteEntry
    ]
    
    # Reset all product entries to 0
    for entry in entries:
        entry.delete(0, END)
        entry.insert(0, 0)
    
    # Clear total and tax entries
    for entry in [cosmetictaxEntry, grocerytaxEntry, drinkstaxEntry,
                 cosmeticpriceEntry, grocerypriceEntry, drinkspriceEntry]:
        entry.delete(0, END)
    
    # Clear customer details
    nameEntry.delete(0, END)
    phoneEntry.delete(0, END)
    billnumberEntry.delete(0, END)
    
    # Clear textarea
    textarea.delete(1.0, END)

def send_email():
    """Function to send bill via email."""
    def send_gmail():
        try:
            ob = smtplib.SMTP('smtp.gmail.com', 587)
            ob.starttls()
            ob.login(senderEntry.get(), passwordEntry.get())
            message = email_textarea.get(1.0, END)
            ob.sendmail(senderEntry.get(), recieverEntry.get(), message)
            ob.quit()
            messagebox.showinfo('Success', 'Bill is successfully sent', parent=root1)
            root1.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'Something went wrong: {str(e)}', parent=root1)
    
    if textarea.get(1.0, END) == '\n':
        messagebox.showerror('Error', 'Bill is empty')
    else:
        root1 = Toplevel()
        root1.grab_set()
        root1.title('Send Gmail')
        root1.config(bg='blue')
        root1.resizable(0, 0)
        
        # Sender Frame
        senderFrame = LabelFrame(root1, text='SENDER', font=('arial', 16, 'bold'), bd=6, bg='blue', fg='white')
        senderFrame.grid(row=0, column=0, padx=40, pady=20)
        
        senderLabel = Label(senderFrame, text="Sender's Email", font=('arial', 14, 'bold'), bg='blue', fg='white')
        senderLabel.grid(row=0, column=0, padx=10, pady=8)
        
        senderEntry = Entry(senderFrame, font=('arial', 14, 'bold'), bd=2, width=23, relief=RIDGE)
        senderEntry.grid(row=0, column=1, padx=10, pady=8)
        
        passwordLabel = Label(senderFrame, text="Password", font=('arial', 14, 'bold'), bg='blue', fg='white')
        passwordLabel.grid(row=1, column=0, padx=10, pady=8)
        
        passwordEntry = Entry(senderFrame, font=('arial', 14, 'bold'), bd=2, width=23, relief=RIDGE, show='*')
        passwordEntry.grid(row=1, column=1, padx=10, pady=8)
        
        # Recipient Frame
        recipientFrame = LabelFrame(root1, text='RECIPIENT', font=('arial', 16, 'bold'), bd=6, bg='blue', fg='white')
        recipientFrame.grid(row=1, column=0, padx=40, pady=20)
        
        recieverLabel = Label(recipientFrame, text="Email Address", font=('arial', 14, 'bold'), bg='blue', fg='white')
        recieverLabel.grid(row=0, column=0, padx=10, pady=8)
        
        recieverEntry = Entry(recipientFrame, font=('arial', 14, 'bold'), bd=2, width=23, relief=RIDGE)
        recieverEntry.grid(row=0, column=1, padx=10, pady=8)
        
        messageLabel = Label(recipientFrame, text="Message", font=('arial', 14, 'bold'), bg='blue', fg='white')
        messageLabel.grid(row=1, column=0, padx=10, pady=8)
        
        email_textarea = Text(recipientFrame, font=('arial', 14, 'bold'), bd=2, relief=SUNKEN, width=42, height=11)
        email_textarea.grid(row=2, column=0, columnspan=2)
        email_textarea.delete(1.0, END)
        email_textarea.insert(END, textarea.get(1.0, END).replace('=','').replace('-','').replace('\t\t\t','\t\t'))
        
        sendButton = Button(root1, text='SEND', font=('arial', 16, 'bold'), width=15, command=send_gmail)
        sendButton.grid(row=2, column=0, pady=20)
        
        root1.mainloop()

def print_bill():
    """Function to print the bill."""
    if textarea.get(1.0, END) == '\n':
        messagebox.showerror('Error', 'Bill is empty')
    else:
        file = tempfile.mktemp('.txt')
        open(file, 'w').write(textarea.get(1.0, END))
        os.startfile(file, 'print')

def search_bill():
    """Search for a bill by bill number."""
    # First try to find in database
    bill_data = db.get_bill(billnumberEntry.get())
    
    if bill_data:
        # Display the bill from database
        display_bill_from_db(bill_data)
    else:
        # Fallback to file search for compatibility with old system
        for i in os.listdir('bills/'):
            if i.split('.')[0] == billnumberEntry.get():
                f = open(f'bills/{i}', 'r')
                textarea.delete('1.0', END)
                for data in f:
                    textarea.insert(END, data)
                f.close()
                break
        else:
            messagebox.showerror('Error', 'Invalid Bill Number')

def display_bill_from_db(bill_data):
    """Display a bill retrieved from database."""
    textarea.delete(1.0, END)
    
    textarea.insert(END, '\t\t**Welcome Customer**\n')
    textarea.insert(END, f'\nBill Number: {bill_data["bill_number"]}\n')
    textarea.insert(END, f'\nCustomer Name: {bill_data["name"]}\n')
    textarea.insert(END, f'\nCustomer Phone Number: {bill_data["phone"]}\n')
    textarea.insert(END, f'\nBill Date: {bill_data["bill_date"]}\n')
    textarea.insert(END, '\n=======================================================')
    textarea.insert(END, 'Product\t\t\tQuantity\t\t\tPrice')
    textarea.insert(END, '\n=======================================================')
    
    for product in bill_data["products"]:
        textarea.insert(END, f'\n{product["product_name"]}\t\t\t{product["quantity"]}\t\t\t{product["price"]} Rs')
    
    textarea.insert(END, '\n-------------------------------------------------------')
    
    if bill_data["cosmetic_tax"] > 0:
        textarea.insert(END, f'\nCosmetic Tax\t\t\t\t{bill_data["cosmetic_tax"]} Rs')
    if bill_data["grocery_tax"] > 0:
        textarea.insert(END, f'\nGrocery Tax\t\t\t\t{bill_data["grocery_tax"]} Rs')
    if bill_data["drinks_tax"] > 0:
        textarea.insert(END, f'\nDrinks Tax\t\t\t\t{bill_data["drinks_tax"]} Rs')
    
    textarea.insert(END, f'\n\nTotal Bill \t\t\t\t {bill_data["total_amount"]}')
    textarea.insert(END, '\n-------------------------------------------------------')
    
    # Update entry fields
    nameEntry.delete(0, END)
    nameEntry.insert(0, bill_data["name"])
    
    phoneEntry.delete(0, END)
    phoneEntry.insert(0, bill_data["phone"])
    
    # Update price entries
    cosmeticpriceEntry.delete(0, END)
    cosmeticpriceEntry.insert(0, f'{bill_data["cosmetic_total"]} Rs')
    
    grocerypriceEntry.delete(0, END)
    grocerypriceEntry.insert(0, f'{bill_data["grocery_total"]} Rs')
    
    drinkspriceEntry.delete(0, END)
    drinkspriceEntry.insert(0, f'{bill_data["drinks_total"]} Rs')
    
    # Update tax entries
    cosmetictaxEntry.delete(0, END)
    cosmetictaxEntry.insert(0, f'{bill_data["cosmetic_tax"]} Rs')
    
    grocerytaxEntry.delete(0, END)
    grocerytaxEntry.insert(0, f'{bill_data["grocery_tax"]} Rs')
    
    drinkstaxEntry.delete(0, END)
    drinkstaxEntry.insert(0, f'{bill_data["drinks_tax"]} Rs')

# Create bills directory if it doesn't exist
if not os.path.exists('bills'):
    os.mkdir('bills')

def save_bill():
    """Save the bill to both file system and database."""
    global billnumber
    result = messagebox.askyesno('Confirm', 'Do you want to save the bill?')
    if result:
        bill_content = textarea.get(1.0, END)
        
        # Save to file (for backwards compatibility)
        file = open(f'bills/{billnumber}.txt', 'w')
        file.write(bill_content)
        file.close()
        
        # Save to database
        bill_data = parse_bill_text_to_db_format(
            bill_content, 
            billnumber,
            nameEntry.get(),
            phoneEntry.get(),
            cosmeticpriceEntry.get(),
            grocerypriceEntry.get(),
            drinkspriceEntry.get(),
            cosmetictaxEntry.get(),
            grocerytaxEntry.get(),
            drinkstaxEntry.get(),
            totalbill
        )
        
        db.add_bill(bill_data)
        
        messagebox.showinfo('Success', f'Bill number {billnumber} is saved successfully')
        billnumber = random.randint(500, 1000)

def parse_bill_text_to_db_format(bill_text, bill_number, customer_name, customer_phone, 
                                cosmetic_price, grocery_price, drinks_price,
                                cosmetic_tax, grocery_tax, drinks_tax, total_bill):
    """Convert bill text to database format for storage."""
    products = []
    product_lines = bill_text.split('\n')
    
    # Categories mapping
    categories = {
        'Bath Soap': 'cosmetic', 'Face Cream': 'cosmetic', 'Face Wash': 'cosmetic',
        'Hair Spray': 'cosmetic', 'Hair Gel': 'cosmetic', 'Body Lotion': 'cosmetic',
        'Rice': 'grocery', 'Oil': 'grocery', 'Daal': 'grocery',
        'Wheat': 'grocery', 'Sugar': 'grocery', 'Tea': 'grocery',
        'Maaza': 'drinks', 'Pepsi': 'drinks', 'Sprite': 'drinks',
        'Dew': 'drinks', 'Frooti': 'drinks', 'Coco Cola': 'drinks'
    }
    
    for line in product_lines:
        parts = line.strip().split('\t\t\t')
        if len(parts) == 3 and parts[0] in categories:
            product_name = parts[0]
            try:
                quantity = int(parts[1])
                # Extract numeric price from "XX Rs"
                price = float(parts[2].split(' ')[0])
                
                products.append({
                    'category': categories[product_name],
                    'name': product_name,
                    'quantity': quantity,
                    'price': price
                })
            except (ValueError, IndexError):
                pass
    
    # Clean up price and tax values (remove "Rs" and convert to float)
    def clean_value(value):
        if isinstance(value, str):
            return float(value.split(' ')[0])
        return float(value)
    
    # Create bill data dictionary
    bill_data = {
        'bill_number': str(bill_number),
        'customer_name': customer_name,
        'customer_phone': customer_phone,
        'cosmetic_price': clean_value(cosmetic_price),
        'grocery_price': clean_value(grocery_price),
        'drinks_price': clean_value(drinks_price),
        'cosmetic_tax': clean_value(cosmetic_tax),
        'grocery_tax': clean_value(grocery_tax),
        'drinks_tax': clean_value(drinks_tax),
        'total_bill': total_bill if isinstance(total_bill, (int, float)) else clean_value(total_bill),
        'products': products
    }
    
    return bill_data

def summarize_total_purchases():
    """Show summary of all purchases from database."""
    stats = db.get_total_sales()
    
    summary_window = Toplevel()
    summary_window.title("Sales Summary")
    summary_window.geometry("600x400")
    summary_window.config(bg='lightblue')
    
    # Create frame for summary
    summary_frame = Frame(summary_window, bg='lightblue', bd=5, relief=RIDGE)
    summary_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Title
    Label(summary_frame, text="SALES SUMMARY", font=('arial', 20, 'bold'), 
          bg='lightblue', fg='navy').pack(pady=10)
    
    # Display statistics
    stats_text = f"""
    Total Number of Bills: {stats['total_bills']}
    
    Category Sales:
    -------------------------
    Cosmetics: {stats['cosmetic_total']:.2f} Rs
    Grocery: {stats['grocery_total']:.2f} Rs
    Drinks: {stats['drinks_total']:.2f} Rs
    
    Category Tax:
    -------------------------
    Cosmetics Tax: {stats['cosmetic_tax']:.2f} Rs
    Grocery Tax: {stats['grocery_tax']:.2f} Rs
    Drinks Tax: {stats['drinks_tax']:.2f} Rs
    
    TOTAL SALES: {stats['total_sales']:.2f} Rs
    """
    
    summary_text = Text(summary_frame, font=('arial', 14), bg='white', fg='black', height=15, width=50)
    summary_text.pack(padx=10, pady=10)
    summary_text.insert(END, stats_text)
    summary_text.config(state=DISABLED)
    
    Button(summary_window, text="CLOSE", command=summary_window.destroy, 
           font=('arial', 16, 'bold'), bg='red', fg='white').pack(pady=10)

def view_all_bills():
    """View all saved bills in a list."""
    bills = db.get_all_bills()
    
    if not bills:
        messagebox.showinfo("Bills", "No bills found in the database")
        return
    
    bills_window = Toplevel()
    bills_window.title("All Bills")
    bills_window.geometry("800x500")
    bills_window.config(bg='lightblue')
    
    # Create frame for bill list
    list_frame = Frame(bills_window, bg='white')
    list_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Create treeview for bills
    columns = ('#1', '#2', '#3', '#4')
    bill_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
    
    # Define headings
    bill_tree.heading('#1', text='Bill Number')
    bill_tree.heading('#2', text='Customer Name')
    bill_tree.heading('#3', text='Amount')
    bill_tree.heading('#4', text='Date')
    
    # Set column widths
    bill_tree.column('#1', width=100, anchor=CENTER)
    bill_tree.column('#2', width=200)
    bill_tree.column('#3', width=100, anchor=E)
    bill_tree.column('#4', width=150)
    
    # Add data to treeview
    for bill in bills:
        bill_tree.insert('', END, values=(
            bill['bill_number'], 
            bill['name'], 
            f"{bill['total_amount']:.2f} Rs", 
            bill['bill_date']
        ))
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=bill_tree.yview)
    bill_tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    bill_tree.pack(fill=BOTH, expand=True)
    
    # Function to view selected bill
    def view_selected_bill():
        selected = bill_tree.focus()
        if selected:
            bill_number = bill_tree.item(selected, 'values')[0]
            billnumberEntry.delete(0, END)
            billnumberEntry.insert(0, bill_number)
            bills_window.destroy()
            search_bill()
    
    # Buttons frame
    button_frame = Frame(bills_window, bg='lightblue')
    button_frame.pack(fill=X, pady=10)
    
    Button(button_frame, text="VIEW BILL", command=view_selected_bill,
           font=('arial', 12, 'bold'), bg='blue', fg='white', width=15).pack(side=LEFT, padx=10)
    
    Button(button_frame, text="CLOSE", command=bills_window.destroy,
           font=('arial', 12, 'bold'), bg='red', fg='white', width=15).pack(side=RIGHT, padx=10)

def bill_area():
    """Create bill in the text area."""
    if nameEntry.get() == '' or phoneEntry.get() == '':
        messagebox.showerror('Error', 'Customer Details Are Required')
    elif cosmeticpriceEntry.get() == '' and grocerypriceEntry.get() == '' and drinkspriceEntry.get() == '':
        messagebox.showerror('Error', 'No Products are selected')
    elif cosmeticpriceEntry.get() == '0 Rs' and grocerypriceEntry.get() == '0 Rs' and drinkspriceEntry.get() == '0 Rs':
        messagebox.showerror('Error', 'No Products are selected')
    else:
        textarea.delete(1.0, END)
        
        # Bill header
        textarea.insert(END, '\t\t**Welcome Customer**\n')
        textarea.insert(END, f'\nBill Number: {billnumber}\n')
        textarea.insert(END, f'\nCustomer Name: {nameEntry.get()}\n')
        textarea.insert(END, f'\nCustomer Phone Number: {phoneEntry.get()}\n')
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        textarea.insert(END, f'\nDate: {current_date}\n')
        textarea.insert(END, '\n=======================================================')
        textarea.insert(END, 'Product\t\t\tQuantity\t\t\tPrice')
        textarea.insert(END, '\n=======================================================')
        
        # Add cosmetic products to bill
        if int(bathsoapEntry.get()) > 0:
            textarea.insert(END, f'\nBath Soap\t\t\t{bathsoapEntry.get()}\t\t\t{soapprice} Rs')
        if int(hairsprayEntry.get()) > 0:
            textarea.insert(END, f'\nHair Spray\t\t\t{hairsprayEntry.get()}\t\t\t{hairsprayprice} Rs')
        if int(hairgelEntry.get()) > 0:
            textarea.insert(END, f'\nHair Gel\t\t\t{hairgelEntry.get()}\t\t\t{hairgelprice} Rs')
        if int(facecreamEntry.get()) > 0:
            textarea.insert(END, f'\nFace Cream\t\t\t{facecreamEntry.get()}\t\t\t{facecreamprice} Rs')
        if int(facewashEntry.get()) > 0:
            textarea.insert(END, f'\nFace Wash\t\t\t{facewashEntry.get()}\t\t\t{facewashprice} Rs')
        if int(bodylotionEntry.get()) > 0:
            textarea.insert(END, f'\nBody Lotion\t\t\t{bodylotionEntry.get()}\t\t\t{bodylotionprice} Rs')
        
        # Add grocery products to bill
        if int(riceEntry.get()) > 0:
            textarea.insert(END, f'\nRice\t\t\t{riceEntry.get()}\t\t\t{riceprice} Rs')
        if int(oilEntry.get()) > 0:
            textarea.insert(END, f'\nOil\t\t\t{oilEntry.get()}\t\t\t{oilprice} Rs')
        if int(sugarEntry.get()) > 0:
            textarea.insert(END, f'\nSugar\t\t\t{sugarEntry.get()}\t\t\t{sugarprice} Rs')
        if int(wheatEntry.get()) > 0:
            textarea.insert(END, f'\nWheat\t\t\t{wheatEntry.get()}\t\t\t{wheatprice} Rs')
        if int(daalEntry.get()) > 0:
            textarea.insert(END, f'\nDaal\t\t\t{daalEntry.get()}\t\t\t{daalprice} Rs')
        if int(teaEntry.get()) > 0:
            textarea.insert(END, f'\nTea\t\t\t{teaEntry.get()}\t\t\t{teaprice} Rs')
        
        # Add drinks to bill
        if int(maazaEntry.get()) > 0:
            textarea.insert(END, f'\nMaaza\t\t\t{maazaEntry.get()}\t\t\t{maazaprice} Rs')
        if int(frootiEntry.get()) > 0:
            textarea.insert(END, f'\nFrooti\t\t\t{frootiEntry.get()}\t\t\t{frootiprice} Rs')
        if int(pepsiEntry.get()) > 0:
            textarea.insert(END, f'\nPepsi\t\t\t{pepsiEntry.get()}\t\t\t{pepsiprice} Rs')
        if int(cococolaEntry.get()) > 0:
            textarea.insert(END, f'\nCoco Cola\t\t\t{cococolaEntry.get()}\t\t\t{cococolaprice} Rs')
        if int(dewEntry.get()) > 0:
            textarea.insert(END, f'\nDew\t\t\t{dewEntry.get()}\t\t\t{dewprice} Rs')
        if int(spriteEntry.get()) > 0:
            textarea.insert(END, f'\nSprite\t\t\t{spriteEntry.get()}\t\t\t{spriteprice} Rs')
        
        # Add tax information
        textarea.insert(END, '\n-------------------------------------------------------')
        
        if cosmetictaxEntry.get() != '0.0 Rs' and cosmetictaxEntry.get() != '':
            textarea.insert(END, f'\nCosmetic Tax\t\t\t\t{cosmetictaxEntry.get()}')
        if grocerytaxEntry.get() != '0.0 Rs' and grocerytaxEntry.get() != '':
            textarea.insert(END, f'\nGrocery Tax\t\t\t\t{grocerytaxEntry.get()}')
        if drinkstaxEntry.get() != '0.0 Rs' and drinkstaxEntry.get() != '':
            textarea.insert(END, f'\nDrinks Tax\t\t\t\t{drinkstaxEntry.get()}')
        
        # Add total
        textarea.insert(END, f'\n\nTotal Bill \t\t\t\t {totalbill}')
        textarea.insert(END, '\n-------------------------------------------------------')
        
        # Save bill
        save_bill()

def total():
    """Calculate the total price and taxes for all items."""
    global soapprice, hairsprayprice, hairgelprice, facecreamprice, facewashprice, bodylotionprice
    global riceprice, daalprice, oilprice, sugarprice, wheatprice, teaprice
    global frootiprice, dewprice, pepsiprice, spriteprice, cococolaprice, maazaprice
    global totalbill
    
    # Cosmetics price calculation
    soapprice = int(bathsoapEntry.get()) * 20
    facecreamprice = int(facecreamEntry.get()) * 50
    facewashprice = int(facewashEntry.get()) * 100
    hairsprayprice = int(hairsprayEntry.get()) * 150
    hairgelprice = int(hairgelEntry.get()) * 80
    bodylotionprice = int(bodylotionEntry.get()) * 60

    totalcosmeticprice = soapprice + facewashprice + facecreamprice + hairgelprice + hairsprayprice + bodylotionprice
    cosmeticpriceEntry.delete(0, END)
    cosmeticpriceEntry.insert(0, f'{totalcosmeticprice} Rs')
    cosmtictax = totalcosmeticprice * 0.12
    cosmetictaxEntry.delete(0, END)
    cosmetictaxEntry.insert(0, str(cosmtictax) + ' Rs')

    # Grocery price calculation
    riceprice = int(riceEntry.get()) * 30
    daalprice = int(daalEntry.get()) * 100
    oilprice = int(oilEntry.get()) * 120
    sugarprice = int(sugarEntry.get()) * 50
    teaprice = int(teaEntry.get()) * 140
    wheatprice = int(wheatEntry.get()) * 80

    totalgroceryprice = riceprice + daalprice + oilprice + sugarprice + teaprice + wheatprice
    grocerypriceEntry.delete(0, END)
    grocerypriceEntry.insert(0, str(totalgroceryprice) + ' Rs')
    grocerytax = totalgroceryprice * 0.05
    grocerytaxEntry.delete(0, END)
    grocerytaxEntry.insert(0, str(grocerytax) + ' Rs')

    # Drinks price calculation
    maazaprice = int(maazaEntry.get()) * 50
    frootiprice = int(frootiEntry.get()) * 20
    dewprice = int(dewEntry.get()) * 30
    pepsiprice = int(pepsiEntry.get()) * 20
    spriteprice = int(spriteEntry.get()) * 45
    cococolaprice = int(cococolaEntry.get()) * 90

    totaldrinksprice = maazaprice + frootiprice + dewprice + pepsiprice + spriteprice + cococolaprice
    drinkspriceEntry.delete(0, END)
    drinkspriceEntry.insert(0, str(totaldrinksprice) + ' Rs')
    drinkstax = totaldrinksprice * 0.08
    drinkstaxEntry.delete(0, END)
    drinkstaxEntry.insert(0, str(drinkstax) + ' Rs')

    # Calculate total bill
    totalbill = totalcosmeticprice + totalgroceryprice + totaldrinksprice + cosmtictax + grocerytax + drinkstax

# GUI Part
root = Tk()
root.title('Retail Billing System')
root.geometry('1270x685')

# Try to load icon if it exists
try:
    root.iconbitmap('icon.ico')
except:
    pass  # Ignore if icon doesn't exist

headingLabel = Label(root, text='Retail Billing System', font=('times new roman', 30, 'bold'),
                     bg='blue', fg='gold', bd=12, relief=GROOVE)
headingLabel.pack(fill=X)

# Customer Details Frame
customer_details_frame = LabelFrame(root, text='Customer Details', font=('times new roman', 15, 'bold'),
                                    fg='gold', bd=8, relief=GROOVE, bg='blue')
customer_details_frame.pack(fill=X)

nameLabel = Label(customer_details_frame, text='Name', font=('times new roman', 15, 'bold'), bg='blue',
                  fg='white')
nameLabel.grid(row=0, column=0, padx=20)

nameEntry = Entry(customer_details_frame, font=('arial', 15), bd=7, width=18)
nameEntry.grid(row=0, column=1, padx=8)

phoneLabel = Label(customer_details_frame, text='Phone Number', font=('times new roman', 15, 'bold'), bg='blue',
                   fg='white')
phoneLabel.grid(row=0, column=2, padx=20, pady=2)

phoneEntry = Entry(customer_details_frame, font=('arial', 15), bd=7, width=18)
phoneEntry.grid(row=0, column=3, padx=8)

billnumberLabel = Label(customer_details_frame, text='Bill Number', font=('times new roman', 15, 'bold'), bg='blue',
                        fg='white')
billnumberLabel.grid(row=0, column=4, padx=20, pady=2)

billnumberEntry = Entry(customer_details_frame, font=('arial', 15), bd=7, width=18)
billnumberEntry.grid(row=0, column=5, padx=8)

searchButton = Button(customer_details_frame, text='SEARCH',
                      font=('arial', 12, 'bold'), bd=7, width=10, command=search_bill)
searchButton.grid(row=0, column=6, padx=20, pady=8)

# Products Frame
productsFrame = Frame(root)
productsFrame.pack()

# Cosmetics Frame
cosmeticsFrame = LabelFrame(productsFrame, text='Cosmetics', font=('times new roman', 15, 'bold'),
                            fg='gold', bd=8, relief=GROOVE, bg='blue')
cosmeticsFrame.grid(row=0, column=0)

bathsoapLabel = Label(cosmeticsFrame, text='Bath Soap', font=('times new roman', 15, 'bold'), bg='blue',
                      fg='white')
bathsoapLabel.grid(row=0, column=0, pady=9, padx=10, sticky='w')

bathsoapEntry = Entry(cosmeticsFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
bathsoapEntry.grid(row=0, column=1, pady=9, padx=10)
bathsoapEntry.insert(0, 0)

facecreamLabel = Label(cosmeticsFrame, text='Face Cream', font=('times new roman', 15, 'bold'), bg='blue',
                       fg='white')
facecreamLabel.grid(row=1, column=0, pady=9, padx=10, sticky='w')

facecreamEntry = Entry(cosmeticsFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
facecreamEntry.grid(row=1, column=1, pady=9, padx=10)
facecreamEntry.insert(0, 0)

facewashLabel = Label(cosmeticsFrame, text='Face Wash', font=('times new roman', 15, 'bold'), bg='blue',
                      fg='white')
facewashLabel.grid(row=2, column=0, pady=9, padx=10, sticky='w')

facewashEntry = Entry(cosmeticsFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
facewashEntry.grid(row=2, column=1, pady=9, padx=10)
facewashEntry.insert(0, 0)

hairsprayLabel = Label(cosmeticsFrame, text='Hair Spray', font=('times new roman', 15, 'bold'), bg='blue',
                       fg='white')
hairsprayLabel.grid(row=3, column=0, pady=9, padx=10, sticky='w')

hairsprayEntry = Entry(cosmeticsFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
hairsprayEntry.grid(row=3, column=1, pady=9, padx=10)
hairsprayEntry.insert(0, 0)

hairgelLabel = Label(cosmeticsFrame, text='Hair Gel', font=('times new roman', 15, 'bold'), bg='blue',
                     fg='white')
hairgelLabel.grid(row=4, column=0, pady=9, padx=10, sticky='w')

hairgelEntry = Entry(cosmeticsFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
hairgelEntry.grid(row=4, column=1, pady=9, padx=10)
hairgelEntry.insert(0, 0)

bodylotionLabel = Label(cosmeticsFrame, text='Body Lotion', font=('times new roman', 15, 'bold'), bg='blue',
                        fg='white')
bodylotionLabel.grid(row=5, column=0, pady=9, padx=10, sticky='w')

bodylotionEntry = Entry(cosmeticsFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
bodylotionEntry.grid(row=5, column=1, pady=9, padx=10)
bodylotionEntry.insert(0, 0)

# Grocery Frame
groceryFrame = LabelFrame(productsFrame, text='Grocery', font=('times new roman', 15, 'bold'),
                          fg='gold', bd=8, relief=GROOVE, bg='blue')
groceryFrame.grid(row=0, column=1)

riceLabel = Label(groceryFrame, text='Rice', font=('times new roman', 15, 'bold'), bg='blue',
                  fg='white')
riceLabel.grid(row=0, column=0, pady=9, padx=10, sticky='w')

riceEntry = Entry(groceryFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
riceEntry.grid(row=0, column=1, pady=9, padx=10)
riceEntry.insert(0, 0)

oilLabel = Label(groceryFrame, text='Oil', font=('times new roman', 15, 'bold'), bg='blue',
                 fg='white')
oilLabel.grid(row=1, column=0, pady=9, padx=10, sticky='w')

oilEntry = Entry(groceryFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
oilEntry.grid(row=1, column=1, pady=9, padx=10)
oilEntry.insert(0, 0)

daalLabel = Label(groceryFrame, text='Daal', font=('times new roman', 15, 'bold'), bg='blue',
                  fg='white')
daalLabel.grid(row=2, column=0, pady=9, padx=10, sticky='w')

daalEntry = Entry(groceryFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
daalEntry.grid(row=2, column=1, pady=9, padx=10)
daalEntry.insert(0, 0)

wheatLabel = Label(groceryFrame, text='Wheat', font=('times new roman', 15, 'bold'), bg='blue',
                   fg='white')
wheatLabel.grid(row=3, column=0, pady=9, padx=10, sticky='w')

wheatEntry = Entry(groceryFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
wheatEntry.grid(row=3, column=1, pady=9, padx=10)
wheatEntry.insert(0, 0)

sugarLabel = Label(groceryFrame, text='Sugar', font=('times new roman', 15, 'bold'), bg='blue',
                   fg='white')
sugarLabel.grid(row=4, column=0, pady=9, padx=10, sticky='w')

sugarEntry = Entry(groceryFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
sugarEntry.grid(row=4, column=1, pady=9, padx=10)
sugarEntry.insert(0, 0)

teaLabel = Label(groceryFrame, text='Tea', font=('times new roman', 15, 'bold'), bg='blue',
                 fg='white')
teaLabel.grid(row=5, column=0, pady=9, padx=10, sticky='w')

teaEntry = Entry(groceryFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
teaEntry.grid(row=5, column=1, pady=9, padx=10)
teaEntry.insert(0, 0)

# Drinks Frame
drinksFrame = LabelFrame(productsFrame, text='Cold Drinks', font=('times new roman', 15, 'bold'),
                         fg='gold', bd=8, relief=GROOVE, bg='blue')
drinksFrame.grid(row=0, column=2)

maazaLabel = Label(drinksFrame, text='Maaza', font=('times new roman', 15, 'bold'), bg='blue',
                   fg='white')
maazaLabel.grid(row=0, column=0, pady=9, padx=10, sticky='w')

maazaEntry = Entry(drinksFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
maazaEntry.grid(row=0, column=1, pady=9, padx=10)
maazaEntry.insert(0, 0)

pepsiLabel = Label(drinksFrame, text='Pepsi', font=('times new roman', 15, 'bold'), bg='blue',
                   fg='white')
pepsiLabel.grid(row=1, column=0, pady=9, padx=10, sticky='w')

pepsiEntry = Entry(drinksFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
pepsiEntry.grid(row=1, column=1, pady=9, padx=10)
pepsiEntry.insert(0, 0)

spriteLabel = Label(drinksFrame, text='Sprite', font=('times new roman', 15, 'bold'), bg='blue',
                    fg='white')
spriteLabel.grid(row=2, column=0, pady=9, padx=10, sticky='w')

spriteEntry = Entry(drinksFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
spriteEntry.grid(row=2, column=1, pady=9, padx=10)
spriteEntry.insert(0, 0)

dewLabel = Label(drinksFrame, text='Dew', font=('times new roman', 15, 'bold'), bg='blue',
                 fg='white')
dewLabel.grid(row=3, column=0, pady=9, padx=10, sticky='w')

dewEntry = Entry(drinksFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
dewEntry.grid(row=3, column=1, pady=9, padx=10)
dewEntry.insert(0, 0)

frootiLabel = Label(drinksFrame, text='Frooti', font=('times new roman', 15, 'bold'), bg='blue',
                    fg='white')
frootiLabel.grid(row=4, column=0, pady=9, padx=10, sticky='w')

frootiEntry = Entry(drinksFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
frootiEntry.grid(row=4, column=1, pady=9, padx=10)
frootiEntry.insert(0, 0)

cococolaLabel = Label(drinksFrame, text='Coco Cola', font=('times new roman', 15, 'bold'), bg='blue',
                      fg='white')
cococolaLabel.grid(row=5, column=0, pady=9, padx=10, sticky='w')

cococolaEntry = Entry(drinksFrame, font=('times new roman', 15, 'bold'), width=10, bd=5)
cococolaEntry.grid(row=5, column=1, pady=9, padx=10)
cococolaEntry.insert(0, 0)

# Bill Frame
billframe = Frame(productsFrame, bd=8, relief=GROOVE)
billframe.grid(row=0, column=3, padx=10)

billareaLabel = Label(billframe, text='Bill Area', font=('times new roman', 15, 'bold'), bd=7, relief=GROOVE)
billareaLabel.pack(fill=X)

scrollbar = Scrollbar(billframe, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)
textarea = Text(billframe, height=18, width=55, yscrollcommand=scrollbar.set)
textarea.pack()
scrollbar.config(command=textarea.yview)

# Bill Menu Frame
billmenuFrame = LabelFrame(root, text='Bill Menu', font=('times new roman', 15, 'bold'),
                           fg='gold', bd=8, relief=GROOVE, bg='blue')
billmenuFrame.pack()

cosmeticpriceLabel = Label(billmenuFrame, text='Cosmetic Price', font=('times new roman', 14, 'bold'), bg='blue',
                           fg='white')
cosmeticpriceLabel.grid(row=0, column=0, pady=6, padx=10, sticky='w')

cosmeticpriceEntry = Entry(billmenuFrame, font=('times new roman', 14, 'bold'), width=10, bd=5)
cosmeticpriceEntry.grid(row=0, column=1, pady=6, padx=10)

grocerypriceLabel = Label(billmenuFrame, text='Grocery Price', font=('times new roman', 14, 'bold'), bg='blue',
                          fg='white')
grocerypriceLabel.grid(row=1, column=0, pady=6, padx=10, sticky='w')

grocerypriceEntry = Entry(billmenuFrame, font=('times new roman', 14, 'bold'), width=10, bd=5)
grocerypriceEntry.grid(row=1, column=1, pady=6, padx=10)

drinkspriceLabel = Label(billmenuFrame, text='Cold Drink Price', font=('times new roman', 14, 'bold'), bg='blue',
                         fg='white')
drinkspriceLabel.grid(row=2, column=0, pady=6, padx=10, sticky='w')

drinkspriceEntry = Entry(billmenuFrame, font=('times new roman', 14, 'bold'), width=10, bd=5)
drinkspriceEntry.grid(row=2, column=1, pady=6, padx=10)

cosmetictaxLabel = Label(billmenuFrame, text='Cosmetic Tax', font=('times new roman', 14, 'bold'), bg='blue',
                         fg='white')
cosmetictaxLabel.grid(row=0, column=2, pady=6, padx=10, sticky='w')

cosmetictaxEntry = Entry(billmenuFrame, font=('times new roman', 14, 'bold'), width=10, bd=5)
cosmetictaxEntry.grid(row=0, column=3, pady=6, padx=10)

grocerytaxLabel = Label(billmenuFrame, text='Grocery Tax', font=('times new roman', 14, 'bold'), bg='blue',
                        fg='white')
grocerytaxLabel.grid(row=1, column=2, pady=6, padx=10, sticky='w')

grocerytaxEntry = Entry(billmenuFrame, font=('times new roman', 14, 'bold'), width=10, bd=5)
grocerytaxEntry.grid(row=1, column=3, pady=6, padx=10)

drinkstaxLabel = Label(billmenuFrame, text='Cold Drink Tax', font=('times new roman', 14, 'bold'), bg='blue',
                       fg='white')
drinkstaxLabel.grid(row=2, column=2, pady=6, padx=10, sticky='w')

drinkstaxEntry = Entry(billmenuFrame, font=('times new roman', 14, 'bold'), width=10, bd=5)
drinkstaxEntry.grid(row=2, column=3, pady=6, padx=10)

buttonFrame = Frame(billmenuFrame, bd=8, relief=GROOVE)
buttonFrame.grid(row=0, column=4, rowspan=3)

# First row of buttons
totalButton = Button(buttonFrame, text='Total', font=('arial', 16, 'bold'), bg='blue', fg='white',
                    bd=5, width=8, pady=10, command=total)
totalButton.grid(row=0, column=0, pady=10, padx=5)

billButton = Button(buttonFrame, text='Bill', font=('arial', 16, 'bold'), bg='blue', fg='white',
                   bd=5, width=8, pady=10, command=bill_area)
billButton.grid(row=0, column=1, pady=10, padx=5)

emailButton = Button(buttonFrame, text='Email', font=('arial', 16, 'bold'), bg='blue', fg='white',
                    bd=5, width=8, pady=10, command=send_email)
emailButton.grid(row=0, column=2, pady=10, padx=5)

# Second row of buttons
printButton = Button(buttonFrame, text='Print', font=('arial', 16, 'bold'), bg='blue', fg='white',
                    bd=5, width=8, pady=10, command=print_bill)
printButton.grid(row=1, column=0, pady=10, padx=5)

clearButton = Button(buttonFrame, text='Clear', font=('arial', 16, 'bold'), bg='blue', fg='white',
                    bd=5, width=8, pady=10, command=clear)
clearButton.grid(row=1, column=1, pady=10, padx=5)

# View all bills button
viewBillsButton = Button(buttonFrame, text='View Bills', font=('arial', 16, 'bold'), bg='green', fg='white',
                       bd=5, width=8, pady=10, command=view_all_bills)
viewBillsButton.grid(row=1, column=2, pady=10, padx=5)

# Third row - Statistics button
statsButton = Button(buttonFrame, text='Statistics', font=('arial', 16, 'bold'), bg='purple', fg='white',
                   bd=5, width=26, pady=10, command=summarize_total_purchases)
statsButton.grid(row=2, column=0, columnspan=3, pady=10, padx=5)

# Start the main event loop
root.mainloop()