from fpdf import FPDF

class Invoice(FPDF):
    
    def header(self):
        # Logo
        #self.image('logo.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Company name
        self.cell(80)
        self.cell(30, 10, 'Dine Delights', 0, 0, 'C')
        # Line break
        self.ln(20)
    
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
    
    def add_info(self, customer_info, invoice_info, transaction_info):
        # Arial bold 12
        self.set_font('Arial', 'B', 12)
        # Customer information
        for key, value in customer_info.items():
            self.cell(60, 10, key, 1)
            self.cell(130, 10, value, 1)
            self.ln()
        # Transaction information
        for key, value in transaction_info.items():
            self.cell(60, 10, key, 1)
            self.cell(130, 10, value, 1)
            self.ln()
        # Invoice information
        for key, value in invoice_info.items():
            self.cell(60, 10, key, 1)
            self.cell(130, 10, value, 1)
            self.ln()
        # Line break
        self.ln(10)
    
    def add_items(self, items, grand_total):
        # Table header
        self.set_font('Arial', 'B', 12)
        self.cell(60, 10, 'Menu name', 1)
        self.cell(40, 10, 'Menu type', 1)
        self.cell(30, 10, 'Quantity', 1)
        self.cell(30, 10, 'Price (RM)', 1)
        self.cell(30, 10, 'Total (RM)', 1)
        self.ln()
        # Table rows
        self.set_font('Arial', '', 12)
        for item in items:
            self.cell(60, 10, item['menu_name'], 1)
            self.cell(40, 10, item['menu_type'], 1)
            self.cell(30, 10, str(item['quantity']), 1)
            self.cell(30, 10, str(item['price']), 1)
            self.cell(30, 10, str(item["total_menu_price"]), 1)
            self.ln()
            
        # Total
        self.cell(160, 10, 'Grand Total (RM)', 1)
        self.cell(30, 10, grand_total, 1)
        self.ln()