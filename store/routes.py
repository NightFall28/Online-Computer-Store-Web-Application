from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from store import app, db, bcrypt, mail, search
from store.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, MemoForm, WalletForm, 
                        AddDesktopForm, AddLaptopForm, AddEdgeComputingForm, SelectProductTypeForm, AddMacbookForm, AddiMacForm,
                        CustomizeDesktopForm, CustomizeLaptopForm, CustomizeEdgeComputingForm, CustomizeMacbookForm,
                        CustomizeiMacForm, AddCommentForm, NewCommunicateForm, CommunicateCommentForm, DisplayPermissionForm,
                        ContactAdminForm, ProcessReportForm, RatingForm)
from flask_login import current_user, login_user, logout_user, login_required
from store.models import (User, Application, UserBlacklist, Memo, Processor, GraphicCard, Memory, HardDrive, Motherboard, Case,
                          Desktop, Laptop, EdgeComputing, EdgeComputingRAM, EdgeComputingDevices, MacbookAir, 
                          MacbookAirRAM, MacbookAirStorage, MacbookList, iMac, iMacAccessoryList, iMacList, iMacMemoryList,
                          iMacStoragelist, CheckoutItem, DesktopComment, LaptopComment, MacbookComment, iMacComment, 
                          EdgeComputingComment, Communicate, CommunicateComment, CustomerMadeDesktop, CustomerMadeDesktopComment,
                          Reports, LaptopProcessor)
from werkzeug.utils import secure_filename
import os
import secrets
from PIL import Image
from flask_mail import Message
from decimal import Decimal

# Set up lists of items for database setup
processor_list = [    
                  {"name": "Intel Core i9-12900K", "company": "Intel", "price": 699},    
                  {"name": "Intel Core i7-12700K", "company": "Intel", "price": 499},    
                  {"name": "Intel Core i5-12600K", "company": "Intel", "price": 319},   
                  {"name": "AMD Ryzen 9 5950X", "company": "AMD", "price": 799},   
                  {"name": "AMD Ryzen 9 5900X", "company": "AMD", "price": 549},    
                  {"name": "AMD Ryzen 7 5800X", "company": "AMD", "price": 399},    
                  {"name": "Intel Core i9-11900K", "company": "Intel", "price": 539},    
                  {"name": "Intel Core i7-11700K", "company": "Intel", "price": 399},    
                  {"name": "Intel Core i5-11600K", "company": "Intel", "price": 259}
            ]

laptop_processor_list = [    
                  {"name": "Intel Core i7-12650HX", "company": "Intel", "price": 472},    
                  {"name": "Intel Core i7-12800HX", "company": "Intel", "price": 502},    
                  {"name": "Intel Core i5-12850HX", "company": "Intel", "price": 428},   
                  {"name": "AMD Ryzen 9 6980HX", "company": "AMD", "price": 699},   
                  {"name": "AMD Ryzen 9 6900HS", "company": "AMD", "price": 449},    
                  {"name": "AMD Ryzen 7 6800U", "company": "AMD", "price": 399},    
                  {"name": "Intel Core i9-12900HX", "company": "Intel", "price": 668},    
                  {"name": "Intel Core i7-12950HX", "company": "Intel", "price": 590},    
                  {"name": "Intel Core i5-12450HX", "company": "Intel", "price": 312}
            ]

graphic_card_list = [    
                     {"name": "Nvidia GeForce RTX 3090", "company": "Nvidia", "price": 1999},    
                     {"name": "Nvidia GeForce RTX 3080 Ti", "company": "Nvidia", "price": 1299},    
                     {"name": "Nvidia GeForce RTX 3070", "company": "Nvidia", "price": 999},    
                     {"name": "AMD Radeon RX 6900 XT", "company": "AMD", "price": 1499},    
                     {"name": "AMD Radeon RX 6800 XT", "company": "AMD", "price": 999},    
                     {"name": "AMD Radeon RX 6700 XT", "company": "AMD", "price": 579},    
                     {"name": "Nvidia GeForce GTX 1660 Super", "company": "Nvidia", "price": 399},    
                     {"name": "Nvidia GeForce GTX 1650", "company": "Nvidia", "price": 149},    
                     {"name": "AMD Radeon RX 5500 XT", "company": "AMD", "price": 219}
                     ]

memory_list = [    
    {"spec": "Corsair Vengeance RGB Pro 32GB DDR4-3600MHz", "company": "Corsair", "price": 189},    
    {"spec": "G.Skill Trident Z Neo 32GB DDR4-3600MHz", "company": "G.Skill", "price": 189},    
    {"spec": "Kingston HyperX Fury RGB 16GB DDR4-3200MHz", "company": "Kingston", "price": 89},    
    {"spec": "Crucial Ballistix 16GB DDR4-3600MHz", "company": "Crucial", "price": 89},    
    {"spec": "Team T-Force Delta RGB 16GB DDR4-3200MHz", "company": "Team Group", "price": 69},    
    {"spec": "Corsair Dominator Platinum RGB 64GB DDR4-3600MHz", "company": "Corsair", "price": 589},    
    {"spec": "G.Skill Ripjaws V 16GB DDR4-3200MHz", "company": "G.Skill", "price": 79},    
    {"spec": "Kingston HyperX Fury 16GB DDR4-2666MHz", "company": "Kingston", "price": 69},    
    {"spec": "Crucial Ballistix Max 64GB DDR4-4000MHz", "company": "Crucial", "price": 559}
    ]

hard_drive_list = [    
    {"spec": "Samsung 980 Pro 2TB NVMe SSD", "company": "Samsung", "price": 699},    
    {"spec": "Western Digital Black SN850 1TB NVMe SSD", "company": "Western Digital", "price": 269},    
    {"spec": "Seagate FireCuda 520 2TB NVMe SSD", "company": "Seagate", "price": 499},    
    {"spec": "Samsung 870 QVO 4TB SATA SSD", "company": "Samsung", "price": 499},    
    {"spec": "Crucial P5 2TB NVMe SSD", "company": "Crucial", "price": 399},  
    {"spec": "Western Digital Blue SN550 1TB NVMe SSD", "company": "Western Digital", "price": 109},   
    {"spec": "Seagate Barracuda 2TB HDD", "company": "Seagate", "price": 59},   
    {"spec": "Toshiba X300 4TB HDD", "company": "Toshiba", "price": 99},   
    {"spec": "Western Digital Black 6TB HDD", "company": "Western Digital", "price": 219}
    ]

motherboard_list = [    
    {"name": "ASUS ROG Maximus XIII Hero Z590 (Intel)", "company": "ASUS", "price": 599, "chipset": "Intel"},    
    {"name": "Gigabyte AORUS X570 Master (AMD)", "company": "Gigabyte", "price": 449, "chipset": "AMD"},    
    {"name": "MSI MPG B550 Gaming Carbon WiFi (AMD)", "company": "MSI", "price": 219, "chipset": "AMD"},    
    {"name": "ASRock B450M Pro4-F (AMD)", "company": "ASRock", "price": 79, "chipset": "AMD"},    
    {"name": "ASUS Prime Z590-P (Intel)", "company": "ASUS", "price": 179, "chipset": "Intel"},    
    {"name": "Gigabyte B560M DS3H (Intel)", "company": "Gigabyte", "price": 99, "chipset": "Intel"},    
    {"name": "MSI MAG X570 Tomahawk WiFi (AMD)", "company": "MSI", "price": 279, "chipset": "AMD"},    
    {"name": "ASRock Z590M Pro4 (Intel)", "company": "ASRock", "price": 159, "chipset": "Intel"},    
    {"name": "ASUS TUF Gaming B550-PLUS (AMD)", "company": "ASUS", "price": 179, "chipset": "AMD"},    
    {"name": "Gigabyte Z590 AORUS Ultra (Intel)", "company": "Gigabyte", "price": 349, "chipset": "Intel"}
    ]

case_list = [    
    {"name": "NZXT H510 Elite", "image_file": "nzxt_h510_elite.jpg", "company": "NZXT", "price": 149},    
    {"name": "Corsair Obsidian Series 500D RGB SE", "image_file": "corsair_obsidian_500d_rgb_se.jpg", "company": "Corsair", "price": 249},    
    {"name": "Phanteks Enthoo Evolv X", "image_file": "phanteks_enthoo_evolv_x.jpg", "company": "Phanteks", "price": 199},    
    {"name": "Fractal Design Meshify C", "image_file": "fractal_design_meshify_c.jpg", "company": "Fractal Design", "price": 99},    
    {"name": "Lian Li O11 Dynamic", "image_file": "lian_li_o11_dynamic.jpg", "company": "Lian Li", "price": 139},    
    {"name": "Cooler Master MasterCase H500M", "image_file": "coolermaster_mastercase_h500m.jpg", "company": "Cooler Master", "price": 219},    
    {"name": "be quiet! Dark Base Pro 900", "image_file": "bequiet_dark_base_pro_900.jpg", "company": "be quiet!", "price": 249},    
    {"name": "Thermaltake Core P5", "image_file": "thermaltake_core_p5.jpg", "company": "Thermaltake", "price": 169},    
    {"name": "In Win 101C", "image_file": "inwin_101c.jpg", "company": "In Win", "price": 89},    
    {"name": "Rosewill Cullinan MX RGB", "image_file": "rosewill_cullinan_mx_rgb.jpg", "company": "Rosewill", "price": 109}
    ]

edge_computing_list = [
     {
        'name': 'Raspberry Pi 4 Model B',
        'processor': 'Broadcom BCM2711, quad-core Cortex-A72 (ARM v8) 64-bit SoC @ 1.5GHz',
        'connectivity': 'Gigabit Ethernet, 2.4 GHz and 5.0 GHz IEEE 802.11ac wireless, Bluetooth 5.0, BLE',
        'ports': '2 × USB 3.0 ports, 2 × USB 2.0 ports, 2 × micro-HDMI ports (up to 4kp60 supported), 3.5 mm audio jack (analog + digital), 2 × MIPI CSI camera ports, 2 × MIPI DSI display ports, 40-pin GPIO header',
        'storage': 'MicroSD card slot for loading operating system and data storage',
        'power': '5V DC via USB-C connector (minimum 3A)',
        'image_file': 'https://m.media-amazon.com/images/I/41tHhdnhS4L._AC_.jpg',
        
    },
    {
        'name': 'NVIDIA Jetson Nano',
        'processor': 'Quad-core ARM Cortex-A57 MPCore processor, NVIDIA Maxwell GPU with 128 CUDA cores',
        
        'connectivity': 'Gigabit Ethernet, 802.11ac wireless, Bluetooth',
        'ports': '4 x USB 3.0, 1 x USB 2.0, HDMI, DisplayPort, CSI camera connector, DSI display connector, GPIO',
        'storage': 'MicroSD card slot for loading operating system and data storage',
        'power': '5V DC via Micro-USB or GPIO',
        'image_file': 'https://www.nvidia.com/content/dam/en-zz/Solutions/intelligent-machines/embedded-systems/jetson-nano/nvidia-jetson-nano-og.jpg',

    },
    {
        'name': 'Intel NUC',
        'processor': 'i7 processor',
        
        'connectivity': 'Gigabit Ethernet, Intel Dual Band Wireless-AC 8265 (802.11ac), Bluetooth 4.2',
        'ports': '2 x HDMI, 4 x USB 3.0, 2 x USB 2.0, Gigabit Ethernet, headphone/mic jack',
        'storage': 'Supports 2.5" SATA SSD/HDD and M.2 NVMe SSD',
        'power': '19V DC via external power adapter',
        'image_file': 'https://www.intel.com/content/dam/www/central-libraries/us/en/images/2022-11/nuc-12-pro-zoom-front-angle-rwd.png.rendition.intel.web.480.270.png',
    },
    {
        'name': 'BeagleBone Black',
        'processor': '1GHz Sitara AM3358BZCZ100 ARM Cortex-A8 processor',
        
        'connectivity': '10/100 Ethernet, USB 2.0, microSD slot',
        'ports': 'USB host, USB device, HDMI output, 2x 46-pin headers',
        'storage': '4GB 8-bit eMMC on-board flash storage',
        'power': '5V DC via USB or DC jack',
        'image_file': 'https://beagleboard.org/static/ti/product_detail_black_lg.jpg',

    },
    {
        'name': 'UP Core',
        'processor': 'Intel Atom x5-Z8350 quad-core processor',
        'RAM': 'Up to 4GB DDR3L-1600',
        'connectivity': 'Gigabit Ethernet, Wi-Fi, Bluetooth 4.0',
        'ports': '2 x USB 2.0, 1 x USB 3.0, HDMI, DP, eDP/LVDS, MIPI-CSI, MIPI-DSI, 40-pin header',
        'storage': 'Up to 64GB eMMC, M.2 2280 slot for SSD',
        'power': '5V DC via barrel jack or 10-pin header',
        'image_file': 'https://up-board.org/wp-content/uploads/2020/12/Upcore-3qtr1_1500x1500.png',
        
    }
]

edge_computing_RAM_list = [
    {
        'name': 'Raspberry Pi 4 Model B',
        'RAM': '2GB LPDDR4-3200 SDRAM',
        'price': 35
    },
    {
        'name': 'Raspberry Pi 4 Model B',
        'RAM': '4GB LPDDR4-3200 SDRAM',
        'price': 55
    },
    {
        'name': 'Raspberry Pi 4 Model B',
        'RAM': '8GB LPDDR4-3200 SDRAM',
        'price': 75
    },
    {
        'name': 'NVIDIA Jetson Nano',
        'RAM': '4GB 64-bit LPDDR4 @ 25.6 GB/s',
        'price': 99
    },
    {
        'name': 'Intel NUC',
        'RAM': '4GB 1.2V DDR4',
        'price': 200
    },
    {
        'name': 'Intel NUC',
        'RAM': '8GB 1.2V DDR4',
        'price': 320
    },
    {
        'name': 'Intel NUC',
        'RAM': '16GB 1.2V DDR4',
        'price': 620
    },
    {
        'name': 'Intel NUC',
        'RAM': '32GB 1.2V DDR4',
        'price': 840
    },
    {
        'name': 'Intel NUC',
        'RAM': '64GB 1.2V DDR4',
        'price': 1000
    },
    {
        'name': 'BeagleBone Black',
        'RAM': '512MB DDR3 RAM',
        'price': 55
    },
    {
        'name': 'UP Core',
        'RAM':"4GB DDR3L-1600",
        'price': 299
    }
]

macbook_list = [
    {
        'name': 'MacBook Air M1 Chip',
        'processor': '8-Core CPU',
        'GPU': '7-Core GPU',
        'display': '13-inch Retina display with True Tone',
        'ports': 'Two Thunderbolt / USB 4 ports',
        'power': '30W USB-C Power Adapter',
        'price': 999
    },
    {
        'name': 'MacBook Air M2 Chip',
        'processor': '8-Core CPU',
        'GPU': '8-Core GPU',
        'display': '13.6-inch Liquid Retina display with True Tone',
        'ports': 'Two Thunderbolt / USB 4 ports',
        'power': '35W Dual USB-C Port Compact Power Adapter',
        'price': 1199
    }
]

macbook_air_storage_list = [
    {
        'hard_drive': '256GB SSD',
        'price': 0
    },
    {
        'hard_drive': '512GB SSD',
        'price': 200
    },
    {
        'hard_drive': '1TB SSD',
        'price': 400
    },
    {
        'hard_drive': '2TB SSD',
        'price': 800
    }
]

macbook_air_RAM_list = [
    {
        'memory': '8GB',
        'price': 0
    },
    {
        'memory': '16GB',
        'price': 200
    },
    {
        'memory': '24GB',
        'price': 400
    }
]

imac_list = [
    {
        'name': '24-inch iMac Apple M1 Chip',
        'processor': '8-core CPU, 16-core Neural Engine',
        'GPU': '7-core GPU',
        'ports': 'Two Thunderbolt / USB 4 ports',
        'price': 1299
    }
]

imac_memory_list = [
    {
        'memory': '8GB',
        'price': 0
    },
    {
        'memory': '16GB',
        'price': 200
    }
]

imac_storage_list = [
    {
        'hard_drive':'256GB',
        'price': 0
    },
    {
        'hard_drive':'512GB',
        'price': 200
    },
    {
        'hard_drive':'1TB',
        'price': 400
    }
]

imac_accessory_list = [
    {
        'accessory':'Magic Mouse',
        'price': 0
    },
    {
        'accessory':'Magic Trackpad',
        'price': 50
    },
    {
        'accessory':'Magic Mouse + Magic Trackpad',
        'price': 129
    }
]



@app.route('/')
@app.route('/home')
def home():
    
    # When first time visiting website with empty database, fill up database with necessary data first
    if User.query.filter(User.email=='neilh200328@gmail.com').first():
        pass
    else:
        hashed_password = bcrypt.generate_password_hash('storeowner').decode('utf-8')
        user = User(name='Store Owner', email='neilh200328@gmail.com', password=hashed_password, is_admin=True,
                    country='United States', state='NY', city='New York', address='666 Random Street',
                            zipcode=54321, image_file="hutao.jpg")
        db.session.add(user)
        db.session.commit()
    # if User.query.filter(User.email=='neilh1334@gmail.com').first():
    #     pass
    # else:
    #     hashed_password = bcrypt.generate_password_hash('12345').decode('utf-8')
    #     user = User(name='Junhui Huang', email='neilh1334@gmail.com', password=hashed_password, is_employee=True,
    #                 country='United States', state='NY', city='New York', address='888 Random Street',
    #                         zipcode=54321)
    #     db.session.add(user)
    #     db.session.commit()
    # if User.query.filter(User.email=='jhuang028@citymail.cuny.edu').first():
    #     pass
    # else:
    #     hashed_password = bcrypt.generate_password_hash('12345').decode('utf-8')
    #     user = User(name='Leo Huang', email='jhuang028@citymail.cuny.edu', password=hashed_password, is_customer=True,
    #                 country='United States', state='NY', city='New York', address='160 Convent Avenue',
    #                         zipcode=10031)
    #     db.session.add(user)
    #     db.session.commit()
    # if User.query.filter(User.email=='tobikyle28@gmail.com').first():
    #     pass
    # else:
    #     hashed_password = bcrypt.generate_password_hash('12345').decode('utf-8')
    #     user = User(name='Lawrence', email='tobikyle28@gmail.com', password=hashed_password, is_customer=True,
    #                 country='United States', state='NY', city='New York', address='Homeless',
    #                         zipcode=54321)
    #     db.session.add(user)
    #     db.session.commit()
    if Processor.query.first():
        pass
    else:
        for processor in processor_list:
            new_processor = Processor(name=processor['name'], company=processor['company'], price=processor['price'])
            db.session.add(new_processor)
            db.session.commit()
    if LaptopProcessor.query.first():
        pass
    else:
        for processor in laptop_processor_list:
            new_processor = LaptopProcessor(name=processor['name'], company=processor['company'], price=processor['price'])
            db.session.add(new_processor)
            db.session.commit()

    if GraphicCard.query.first():
        pass
    else:
        for thing in graphic_card_list:
            new_thing = GraphicCard(name=thing['name'], company=thing['company'], price=thing['price'])
            db.session.add(new_thing)
            db.session.commit()
    
    if Memory.query.first():
        pass
    else:
        for thing in memory_list:
            new_thing = Memory(spec=thing['spec'], company=thing['company'], price=thing['price'])
            db.session.add(new_thing)
            db.session.commit()

    if HardDrive.query.first():
        pass
    else:
        for thing in hard_drive_list:
            new_thing = HardDrive(spec=thing['spec'], company=thing['company'], price=thing['price'])
            db.session.add(new_thing)
            db.session.commit()
    
    if Motherboard.query.first():
        pass
    else:
        for thing in motherboard_list:
            new_thing = Motherboard(name=thing['name'], company=thing['company'], price=thing['price'], chipset=thing['chipset'])
            db.session.add(new_thing)
            db.session.commit()

    if Case.query.first():
        pass
    else:
        for thing in case_list:
            new_thing = Case(image_file=thing["image_file"], name=thing['name'], company=thing['company'], price=thing['price'])
            db.session.add(new_thing)
            db.session.commit()

    if EdgeComputingRAM.query.first():
        pass
    else:
        for thing in edge_computing_RAM_list:
            new_thing = EdgeComputingRAM(name=thing['name'], RAM=thing['RAM'], price=thing['price'])
            db.session.add(new_thing)
            db.session.commit()

    if EdgeComputingDevices.query.first():
        pass
    else:
        for thing in edge_computing_list:
            new_thing = EdgeComputingDevices(name=thing['name'], processor=thing['processor'], connectivity=thing['connectivity'],
                                             ports=thing['ports'], storage=thing['storage'], power=thing['power'])
            db.session.add(new_thing)
            db.session.commit()

    if MacbookAirRAM.query.first():
        pass
    else:
        for thing in macbook_air_RAM_list:
            new_thing = MacbookAirRAM(memory=thing['memory'], price=thing['price'])
            db.session.add(new_thing)
            db.session.commit()

    if MacbookAirStorage.query.first():
        pass
    else:
        for thing in macbook_air_storage_list:
            new_thing = MacbookAirStorage(hard_drive=thing['hard_drive'], price=thing['price'])
            db.session.add(new_thing)
            db.session.commit()

    if MacbookList.query.first():
        pass
    else:
        for thing in macbook_list:
            new_thing = MacbookList(name=thing['name'], price=thing['price'], processor=thing['processor'], GPU=thing['GPU'],
                                    display=thing['display'], ports=thing['ports'], power=thing['power'])
            db.session.add(new_thing)
            db.session.commit()

    if iMacList.query.first():
        pass
    else:
        for thing in imac_list:
            new_thing = iMacList(name=thing['name'], price=thing['price'], processor=thing['processor'], GPU=thing['GPU'],
                                    ports=thing['ports'])
            db.session.add(new_thing)
            db.session.commit()

    if iMacAccessoryList.query.first():
        pass
    else:
        for thing in imac_accessory_list:
            new_thing = iMacAccessoryList(accessory=thing['accessory'], price=thing['price'])
            db.session.add(new_thing)
            db.session.commit()

    if iMacMemoryList.query.first():
        pass
    else:
        for thing in imac_memory_list:
            new_thing = iMacMemoryList(memory=thing['memory'], price=thing['price'])
            db.session.add(new_thing)
            db.session.commit()

    if iMacStoragelist.query.first():
        pass
    else:
        for thing in imac_storage_list:
            new_thing = iMacStoragelist(hard_drive=thing['hard_drive'], price=thing['price'])
            db.session.add(new_thing)
            db.session.commit()

    edge_computings = EdgeComputing.query.order_by(EdgeComputing.rating_5.desc())
    desktops = Desktop.query.order_by(Desktop.rating_5.desc())
    laptops = Laptop.query.order_by(Laptop.rating_5.desc())
    macbooks = MacbookAir.query.order_by(MacbookAir.rating_5.desc())
    imacs = iMac.query.order_by(iMac.rating_5.desc())
    customer_made_desktops = CustomerMadeDesktop.query.order_by(CustomerMadeDesktop.rating_5.desc())

    # pass in store items for display
    return render_template('home.html', desktops=desktops, laptops=laptops,
                           edge_computings=edge_computings, macbooks=macbooks, imacs=imacs, 
                           customer_made_desktops=customer_made_desktops)

@app.route('/desktop')
def desktop():
    desktops = Desktop.query.order_by(Desktop.rating_5.desc())
    imacs = iMac.query.order_by(iMac.rating_5.desc())
    customer_made_desktops = CustomerMadeDesktop.query.order_by(CustomerMadeDesktop.rating_5.desc())
    return render_template('desktop.html', desktops=desktops, imacs=imacs, customer_made_desktops=customer_made_desktops)

@app.route('/laptop')
def laptop():
    laptops = Laptop.query.order_by(Laptop.rating_5.desc())
    macbooks = MacbookAir.query.order_by(MacbookAir.rating_5.desc())
    return render_template('laptop.html', laptops=laptops, macbooks=macbooks)

@app.route('/edge_computing')
def edge_computing():
    edge_computings = EdgeComputing.query.order_by(EdgeComputing.rating_5.desc())
    return render_template('edge_computing.html', edge_computings=edge_computings)


@app.route("/search_result", methods=['GET','POST'])
def search_result():
    search_word = request.args.get('q')
    desktops = Desktop.query.msearch(search_word, fields=['name'])
    imacs = iMac.query.msearch(search_word, fields=['name'])
    customer_made_desktops = CustomerMadeDesktop.query.msearch(search_word, fields=['name'])
    laptops = Laptop.query.msearch(search_word, fields=['name'])
    macbooks = MacbookAir.query.msearch(search_word, fields=['name'])
    edge_computings = EdgeComputing.query.msearch(search_word, fields=['name'])

    return render_template('search_result.html', desktops=desktops, imacs=imacs, customer_made_desktops=customer_made_desktops,
                            laptops=laptops, macbooks=macbooks, edge_computings=edge_computings)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        blacklisted_user = UserBlacklist.query.filter_by(user_blacklisted_email=form.email.data).first()
        if blacklisted_user:
            flash('The email entered has been blacklisted')
            return redirect(url_for('register'))
        user = Application.query.filter_by(email=form.email.data).first()
        if user:
            if user.is_pending:
                flash('Your application still under review. We will notify you through email')
                return redirect(url_for('register'))
       
        user2 = Application(name=form.name.data, email=form.email.data, position=form.position.data,
                            country=form.country.data, state=form.state.data, city=form.city.data, address=form.address.data,
                            zipcode=form.zipcode.data)
        db.session.add(user2) 
        db.session.commit()
        flash('Your application has been sent.', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user1 = UserBlacklist.query.filter_by(user_blacklisted_email=form.email.data).first()
        if user1:
            flash('Your account has been blacklisted. Please contact employee for assistance')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.country = form.country.data
        current_user.state = form.state.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.zipcode = form.zipcode.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.country.data = current_user.country
        form.state.data = current_user.state
        form.city.data = current_user.city
        form.address.data = current_user.address
        form.zipcode.data = current_user.zipcode
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/account/wallet", methods=['GET', 'POST'])
@login_required
def wallet():
    if current_user.is_customer:
        form = WalletForm()
        if form.validate_on_submit():
            current_user.money += form.deposit_amount.data
            db.session.commit()
            flash('Your deposit was successful!', 'success')
            return redirect(url_for('wallet'))
        return render_template('wallet.html', form=form)
    

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route("/application_list")
@login_required
def applications():
    if current_user.is_admin:
        applications = Application.query.filter_by(is_pending=True).all()
        if applications:
            return render_template('application_list.html', applications=applications)
        else:
            flash('No more applications.', 'info')
            return render_template('application_list.html', applications=applications)
    elif current_user.is_employee:
        applications = Application.query.filter_by(is_pending=True, position='Customer').all()
        if applications:
            return render_template('application_list.html', applications=applications)
        else:
            flash('No more applications.', 'info')
            return render_template('application_list.html', applications=applications)

@app.route("/application_list/<int:application_id>")
def application(application_id):
    if current_user.is_admin or current_user.is_employee:
        application = Application.query.get_or_404(application_id)
        return render_template('application.html', title=application.email, application=application)

@app.route("/application_list/<int:application_id>/approve", methods=['POST'])
@login_required
def approve_application(application_id):
    if current_user.is_admin or current_user.is_employee:
        application = Application.query.get_or_404(application_id)
        if application.position == 'Employee':
            user = User(name=application.name, email=application.email, password="$2b$12$xRMPe9Z7xLW6f83Ddv4pBeUCnnd8SV8IZvtmX7FwFHsbFd3fQf6Ke", 
                        is_employee=True, country=application.country, state=application.state, city=application.city,
                        address=application.address, zipcode=application.zipcode)
        elif application.position == 'Customer':
            user = User(name=application.name, email=application.email, password="$2b$12$xRMPe9Z7xLW6f83Ddv4pBeUCnnd8SV8IZvtmX7FwFHsbFd3fQf6Ke", 
                        is_customer=True, country=application.country, state=application.state, city=application.city,
                        address=application.address, zipcode=application.zipcode)
        db.session.add(user)
        application.is_pending = False
        db.session.delete(application)
        db.session.commit()
        user2 = User.query.filter_by(email=user.email).first()
        send_approvedApplication_email(user2)
        flash('The application has been approved.','success')
        return redirect(url_for('applications'))

@app.route("/application_list/<int:application_id>/reject", methods=['POST'])
@login_required
def reject_application(application_id):
    if current_user.is_admin or current_user.is_employee:
        #user = ApplicationBlacklist(application_id=application_id)
        #db.session.add(user)
        #application.is_pending = False
        application = Application.query.get_or_404(application_id)
        db.session.delete(application)
        db.session.commit()
        msg = Message('Your Application was Rejected',
                  sender='noreply@demo.com',
                  recipients=[application.email, 'neilh200328@gmail.com'])
        msg.body = f'''Dear
    {application.name}
        Your Application has been has been rejected.
        Please contact neilh200328@gmail.com for appeal.
        Computer Tech
        '''
        mail.send(msg)

        flash('The application has been rejected.','success')
        return redirect(url_for('applications'))
    
@app.route("/application_list/<int:application_id>/reject/memo", methods=['POST'])
@login_required
def reject_memo(application_id):
    if current_user.is_admin or current_user.is_employee:
        form = MemoForm()
        if form.validate_on_submit():
            memo = Memo(title=form.title.data, content=form.content.data, user_id=current_user.id)
            application = Application.query.get_or_404(application_id)
            db.session.delete(application)
            db.session.add(memo)
            db.session.commit()
            msg = Message('Your Application was Rejected',
                  sender='noreply@demo.com',
                  recipients=[application.email, 'neilh200328@gmail.com'])
            msg.body = f'''Dear
        {application.name}
            Your Application has been has been rejected.
            Please contact store owner for appeal.
            Computer Tech
            '''
            mail.send(msg)
            flash('The application has been rejected, and a memo is sent to admin', 'success')
            return redirect(url_for('applications'))
        return render_template('reject_memo.html', title='Reject Memo', form=form, legend='New Memo')

def send_approvedApplication_email(user):
    token = user.get_reset_token()
    msg = Message('Your Application was Approved',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''Congratulations! Your Application has been reviewed and has been approved. To set your new password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
Welcome to Computer Tech
'''
    mail.send(msg)

@app.route("/admin")
@login_required
def admin():
    return render_template('admin.html', title='Admin')

@app.route('/user_blacklist', methods=['POST', 'GET'])
@login_required
def user_blacklist():
    if current_user.is_admin:
        if request.method == 'POST':
            user_email = request.form['content']
            #user = User.query.filter_by(email=user_email).first()
            #if user:
            new_user = UserBlacklist(user_blacklisted_email=user_email)
            User.query.filter_by(email=user_email).first().is_blacklisted = True
            db.session.add(new_user)
            db.session.commit()
            return redirect('user_blacklist')
            # else:
            #     flash('No user with that email.','info')
            #     return redirect('user_blacklist')
        users = UserBlacklist.query.order_by(UserBlacklist.id).all()
        return render_template('user_blacklist.html', users=users)

@app.route('/remove_blacklisted_user/<int:id>',methods=['POST', 'GET'])
@login_required
def remove_blacklisted_user(id):
    if current_user.is_admin:
        user = UserBlacklist.query.filter_by(id=id).first_or_404()
        if User.query.filter_by(email=user.user_blacklisted_email).first():
            User.query.filter_by(email=user.user_blacklisted_email).first().is_blacklisted = False
            User.query.filter_by(email=user.user_blacklisted_email).first().warning -= 3
        db.session.delete(user)
        db.session.commit()
        flash('User removed from the blacklist','success')
        return redirect(url_for('user_blacklist'))
    
@app.route("/memo")
@login_required
def memo():
    if current_user.is_admin:
        page = request.args.get('page', 1, type=int)
        memos = Memo.query.order_by(Memo.date_posted.desc()).paginate(page=page, per_page=5)
        return render_template('memo.html', memos=memos)

@app.route("/memo/<int:memo_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_memo(memo_id):
    if current_user.is_admin:
        memo = Memo.query.get_or_404(memo_id)
        db.session.delete(memo)
        db.session.commit()
        flash('Memo Deleted', 'success')
        return redirect(url_for('memo'))
    
@app.route("/user_list", methods=['POST', 'GET'])
@login_required
def user_list():
    if current_user.is_admin:
        users = User.query.order_by(User.id)
        return render_template('user_list.html', users=users)
    
@app.route("/user_list/<int:user_id>/delete", methods=['POST', 'GET'])
@login_required
def remove_user(user_id):
    if current_user.is_admin:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('The User has been removed from the system', 'success')
        return redirect(url_for('user_list'))
    
@app.route("/add_product", methods=['POST','GET'])
@login_required
def select_product():
    if current_user.is_employee:
        form = SelectProductTypeForm()
        if form.validate_on_submit():
            if form.computer_type.data == 'Desktop':
                return redirect(url_for('add_desktop'))
            elif form.computer_type.data == 'Laptop':
                return redirect(url_for('add_laptop'))
            elif form.computer_type.data == 'Edge Computing':
                return redirect(url_for('add_edge_computing'))
            elif form.computer_type.data == 'MacBook':
                return redirect(url_for('add_macbook'))
            elif form.computer_type.data == 'iMac':
                return redirect(url_for('add_imac'))
        return render_template('select_product.html', form=form)
    
@app.route("/add_product/macbook", methods=['GET', 'POST'])
@login_required
def add_macbook():
    if current_user.is_employee:
        form = AddMacbookForm()

        form.name.choices = [(g.name, g.name) for g in MacbookList.query.all()]
        form.memory.choices = [(g.memory, g.memory) for g in MacbookAirRAM.query.all()]
        form.storage.choices = [(g.hard_drive, g.hard_drive) for g in MacbookAirStorage.query.all()]

        if form.validate_on_submit():
            file = form.image_file.data
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
    
            macbookair = MacbookAir(name=form.name.data, processor=MacbookList.query.filter_by(name=form.name.data).first().processor,
                                    GPU=MacbookList.query.filter_by(name=form.name.data).first().GPU,
                                    memory=form.memory.data, hard_drive=form.storage.data,
                                    display=MacbookList.query.filter_by(name=form.name.data).first().display,
                                    ports=MacbookList.query.filter_by(name=form.name.data).first().ports,
                                    power=MacbookList.query.filter_by(name=form.name.data).first().power,
                                    price=MacbookList.query.filter_by(name=form.name.data).first().price +
                                          MacbookAirRAM.query.filter_by(memory=form.memory.data).first().price +
                                          MacbookAirStorage.query.filter_by(hard_drive=form.storage.data).first().price,
                                    image_file=file.filename, creator_id=current_user.id)
            db.session.add(macbookair)
            db.session.commit()
            flash('Product Added', 'success')
            return redirect(url_for('home'))
        return render_template('add_macbook.html', form=form)
    
@app.route("/add_product/imac", methods=['GET', 'POST'])
@login_required
def add_imac():
    if current_user.is_employee:
        form = AddiMacForm()

        form.name.choices = [(g.name, g.name) for g in iMacList.query.all()]
        form.memory.choices = [(g.memory, g.memory) for g in iMacMemoryList.query.all()]
        form.storage.choices = [(g.hard_drive, g.hard_drive) for g in iMacStoragelist.query.all()]
        form.accessory.choices = [(g.accessory, g.accessory) for g in iMacAccessoryList.query.all()]

        if form.validate_on_submit():
            file = form.image_file.data
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
    
            imac = iMac(name=form.name.data, processor=iMacList.query.filter_by(name=form.name.data).first().processor,
                        GPU=iMacList.query.filter_by(name=form.name.data).first().GPU,
                        color=form.color.data, ports=iMacList.query.filter_by(name=form.name.data).first().ports,
                        memory=iMacMemoryList.query.filter_by(memory=form.memory.data).first().memory,
                        hard_drive=iMacStoragelist.query.filter_by(hard_drive=form.storage.data).first().hard_drive,
                        accessory=iMacAccessoryList.query.filter_by(accessory=form.accessory.data).first().accessory,
                        image_file=file.filename,
                        price=iMacList.query.filter_by(name=form.name.data).first().price +
                            iMacAccessoryList.query.filter_by(accessory=form.accessory.data).first().price +
                            iMacStoragelist.query.filter_by(hard_drive=form.storage.data).first().price +
                            iMacMemoryList.query.filter_by(memory=form.memory.data).first().price
                            ,creator_id=current_user.id)
            db.session.add(imac)
            db.session.commit()
            flash('Product Added', 'success')
            return redirect(url_for('home'))
        return render_template('add_imac.html', form=form)

    
@app.route("/add_product/desktop", methods=['POST','GET'])
@login_required
def add_desktop():
    if current_user.is_employee:
        form = AddDesktopForm()
        # Populate all choices first
        form.motherboard.choices = [None]+[g.name for g in Motherboard.query.all()]
        form.processor.choices = [(processor.name, processor.name) for processor in Processor.query.all()]
        form.graphic_card.choices = [g.name for g in GraphicCard.query.order_by('name')]
        form.memory.choices = [g.spec for g in Memory.query.order_by('spec')]
        form.hard_drive.choices = [g.spec for g in HardDrive.query.order_by('spec')]
        form.case.choices = [g.name for g in Case.query.order_by('name')]

        if form.validate_on_submit():
            desktop = Desktop(name=form.name.data, processor=form.processor.data, graphic_card=form.graphic_card.data,
                                operating_system=form.operating_system.data, memory=form.memory.data, hard_drive=form.hard_drive.data,
                                motherboard=form.motherboard.data, case=form.case.data, category=form.category.data,
                                price=Processor.query.filter_by(name=form.processor.data).first().price + 
                                    GraphicCard.query.filter_by(name=form.graphic_card.data).first().price +
                                    Memory.query.filter_by(spec=form.memory.data).first().price +
                                    HardDrive.query.filter_by(spec=form.hard_drive.data).first().price +
                                    Motherboard.query.filter_by(name=form.motherboard.data).first().price +
                                    Case.query.filter_by(name=form.case.data).first().price,
                                    image_file=Case.query.filter_by(name=form.case.data).first().image_file
                                    ,creator_id=current_user.id)
            db.session.add(desktop)
            db.session.commit()
            flash('Product Added', 'success')
            return redirect(url_for('home'))
            
        return render_template('add_desktop.html', form=form)
    
@app.route('/add_product/desktop/<motherboard>')
def processor(motherboard):
    if '(Intel)' in motherboard: 
        processors = Processor.query.filter_by(company='Intel').all()
    elif '(AMD)' in motherboard:
        processors = Processor.query.filter_by(company='AMD').all()
    else:
        return jsonify({'Processors': []})
    processorsArray = []
    for g in processors:
        obj = {}
        obj['id'] = g.id
        obj['name'] = g.name
        obj['company'] = g.company
        processorsArray.append(obj)
    return jsonify({'Processors': processorsArray})


@app.route("/add_product/laptop", methods=['POST','GET'])
@login_required
def add_laptop():
    if current_user.is_employee:
        form = AddLaptopForm()
        # Populate all choices first
        form.processor.choices = [processor.name for processor in LaptopProcessor.query.order_by('name')]
        form.graphic_card.choices = [g.name for g in GraphicCard.query.order_by('name')]
        form.memory.choices = [g.spec for g in Memory.query.order_by('spec')]
        form.hard_drive.choices = [g.spec for g in HardDrive.query.order_by('spec')]

        if form.validate_on_submit():
            file = form.image_file.data
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            laptop = Laptop(name=form.name.data, processor=form.processor.data, graphic_card=form.graphic_card.data,
                            operating_system=form.operating_system.data, memory=form.memory.data, hard_drive=form.hard_drive.data,
                            price=LaptopProcessor.query.filter_by(name=form.processor.data).first().price + 
                                GraphicCard.query.filter_by(name=form.graphic_card.data).first().price +
                                Memory.query.filter_by(spec=form.memory.data).first().price +
                                HardDrive.query.filter_by(spec=form.hard_drive.data).first().price,
                                image_file=file.filename
                                ,creator_id=current_user.id)
                                  
            db.session.add(laptop)
            db.session.commit()
            flash('Product Added', 'success')
            return redirect(url_for('home'))

        return render_template('add_laptop.html', form=form)


@app.route("/add_product/edge_computing", methods=['GET','POST'])
@login_required
def add_edge_computing():
    if current_user.is_employee:
        form = AddEdgeComputingForm()
        # Populate all choices first
        form.name.choices = [None]+[g.name for g in EdgeComputingDevices.query.all()]
        form.RAM.choices = [(g.RAM, g.RAM) for g in EdgeComputingRAM.query.all()]

        if form.validate_on_submit(): 
            file = form.image_file.data
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
    
            edge_computing = EdgeComputing(name=form.name.data, 
                                           processor=EdgeComputingDevices.query.filter_by(name=form.name.data).first().processor,
                                           RAM=form.RAM.data,
                                           connectivity=EdgeComputingDevices.query.filter_by(name=form.name.data).first().connectivity,
                                           ports=EdgeComputingDevices.query.filter_by(name=form.name.data).first().ports,
                                           storage=EdgeComputingDevices.query.filter_by(name=form.name.data).first().storage,
                                           power=EdgeComputingDevices.query.filter_by(name=form.name.data).first().power,
                                           image_file=file.filename,
                                           price=EdgeComputingRAM.query.filter_by(RAM=form.RAM.data).first().price,
                                           creator_id=current_user.id)
            db.session.add(edge_computing)
            db.session.commit()
            flash('Product Added', 'success')
            return redirect(url_for('home'))

        return render_template('add_edge_computing.html', form=form)

@app.route('/add_product/edge_computing/<name>')
def RAM(name):
    RAMs = EdgeComputingRAM.query.filter_by(name=name).all()
    RAMsArray = []
    for g in RAMs:
        obj = {}
        obj['id'] = g.id
        obj['RAM'] = g.RAM
        RAMsArray.append(obj)
    return jsonify({'RAMs': RAMsArray})


@app.route("/delete_desktop/<int:desktop_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_desktop(desktop_id):
    if current_user.is_employee:
        desktop = Desktop.query.get_or_404(desktop_id)
        comments = DesktopComment.query.filter_by(desktop_id=desktop_id).all()
        for i in comments:
            db.session.delete(i)
        db.session.delete(desktop)
        db.session.commit()
        flash('Desktop Deleted', 'success')
        return redirect(url_for('home'))
    
@app.route("/delete_laptop/<int:laptop_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_laptop(laptop_id):
    if current_user.is_employee:
        laptop = Laptop.query.get_or_404(laptop_id)
        comments = LaptopComment.query.filter_by(laptop_id=laptop_id).all()
        for i in comments:
            db.session.delete(i)
        db.session.delete(laptop)
        db.session.commit()
        flash('Laptop Deleted', 'success')
        return redirect(url_for('home'))
    
@app.route("/delete_edge_computing/<int:edge_computing_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_edge_computing(edge_computing_id):
    if current_user.is_employee:
        edge_computing = EdgeComputing.query.get_or_404(edge_computing_id)
        db.session.delete(edge_computing)
        db.session.commit()
        flash('Edge Computing Device Deleted', 'success')
        return redirect(url_for('home'))
    
@app.route("/delete_macbook/<int:macbook_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_macbook(macbook_id):
    if current_user.is_employee:
        macbook = MacbookAir.query.get_or_404(macbook_id)
        db.session.delete(macbook)
        db.session.commit()
        flash('Macbook Deleted', 'success')
        return redirect(url_for('home'))
    
@app.route("/delete_imac/<int:imac_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_imac(imac_id):
    if current_user.is_employee:
        imac = iMac.query.get_or_404(imac_id)
        db.session.delete(imac)
        db.session.commit()
        flash('iMac Deleted', 'success')
        return redirect(url_for('home'))

@app.route("/process_checkout/<int:checkout_id>", methods=['GET','POST'])
@login_required
def process_checkout(checkout_id):
    if current_user.is_customer:
        price = CheckoutItem.query.filter_by(id=checkout_id).first().price
        if (current_user.money - price) >= 0:
            current_user.money -= price
            CheckoutItem.query.filter_by(id=checkout_id).first().is_checkedout = True
            current_user.has_discount = False
            db.session.commit()
            msg = Message('Your Order Is Placed', sender='noreply@demo.com',
                            recipients=[current_user.email])
            msg.body = f'''Dear {current_user.name}
            Your order for {CheckoutItem.query.filter_by(id=checkout_id).first().item_name} is placed.
            Cost: ${price}
            Order ID: {checkout_id}
            Please contact an employee for any concern.
            Computer Tech
            '''
            mail.send(msg)
            flash('Purchase Success. Check Email For Receipt', 'success')
            if CheckoutItem.query.filter_by(id=checkout_id).first().madeby_customer:
                return redirect(url_for('display_permission'))
            elif CheckoutItem.query.filter_by(id=checkout_id).first().is_desktop:
                return redirect(url_for('rate_desktop_configuration',desktop_id=CheckoutItem.query.filter_by(id=checkout_id).first().config_id))
            elif CheckoutItem.query.filter_by(id=checkout_id).first().is_laptop:
                return redirect(url_for('rate_laptop_configuration',laptop_id=CheckoutItem.query.filter_by(id=checkout_id).first().config_id))
            elif CheckoutItem.query.filter_by(id=checkout_id).first().is_macbook:
                return redirect(url_for('rate_macbook_configuration',macbook_id=CheckoutItem.query.filter_by(id=checkout_id).first().config_id))
            elif CheckoutItem.query.filter_by(id=checkout_id).first().is_imac:
                return redirect(url_for('rate_imac_configuration',imac_id=CheckoutItem.query.filter_by(id=checkout_id).first().config_id))
            elif CheckoutItem.query.filter_by(id=checkout_id).first().is_edge_computing:
                return redirect(url_for('rate_edge_computing_configuration',edge_computing_id=CheckoutItem.query.filter_by(id=checkout_id).first().config_id))
            elif CheckoutItem.query.filter_by(id=checkout_id).first().is_customer_desktop:
                return redirect(url_for('rate_customer_desktop_configuration',desktop_id=CheckoutItem.query.filter_by(id=checkout_id).first().config_id))
        else:
            current_user.warning += 1
            db.session.commit()
            flash('Balance Exceeded! Please deposit money first', 'error')
            return redirect(url_for('account'))
    
@app.route("/checkout/<int:checkout_id>", methods=['GET','POST'])
@login_required
def checkout(checkout_id):
    if current_user.is_customer:
        price = CheckoutItem.query.filter_by(id=checkout_id).first().price
        return render_template('checkout.html', item=CheckoutItem.query.filter_by(id=checkout_id).first().item_name, price=price,
                               id=checkout_id)

@app.route("/product_detail/<int:desktop_id>/desktop", methods=['POST','GET'])
def desktop_detail(desktop_id):
    desktop = Desktop.query.get_or_404(desktop_id)
    form = CustomizeDesktopForm()

    form.motherboard.choices = [None]+[g.name for g in Motherboard.query.all()]
    form.processor.choices = [(processor.name, processor.name) for processor in Processor.query.all()]
    form.graphic_card.choices = [g.name for g in GraphicCard.query.order_by('name')]
    form.memory.choices = [g.spec for g in Memory.query.order_by('spec')]
    form.hard_drive.choices = [g.spec for g in HardDrive.query.order_by('spec')]
    form.case.choices = [g.name for g in Case.query.order_by('name')]

    if form.validate_on_submit():    
        if current_user.is_authenticated and current_user.is_customer:
            if current_user.has_discount:
                new_price = (Processor.query.filter_by(name=form.processor.data).first().price + 
                    GraphicCard.query.filter_by(name=form.graphic_card.data).first().price +
                    Memory.query.filter_by(spec=form.memory.data).first().price +
                    HardDrive.query.filter_by(spec=form.hard_drive.data).first().price +
                    Motherboard.query.filter_by(name=form.motherboard.data).first().price +
                    Case.query.filter_by(name=form.case.data).first().price) * Decimal(0.9)
            else:
                new_price = (Processor.query.filter_by(name=form.processor.data).first().price + 
                        GraphicCard.query.filter_by(name=form.graphic_card.data).first().price +
                        Memory.query.filter_by(spec=form.memory.data).first().price +
                        HardDrive.query.filter_by(spec=form.hard_drive.data).first().price +
                        Motherboard.query.filter_by(name=form.motherboard.data).first().price +
                        Case.query.filter_by(name=form.case.data).first().price)
            
            checkout_item = CheckoutItem(item_name=desktop.name, price=new_price, config_id=desktop.id, is_desktop=True)
            db.session.add(checkout_item)
            db.session.commit()
            id = CheckoutItem.query.order_by(CheckoutItem.id.desc()).first().id
            return redirect(url_for('checkout',checkout_id=id))

    elif request.method == 'GET':
        form.motherboard.data = desktop.motherboard
        form.processor.data = desktop.processor
        form.graphic_card.data = desktop.graphic_card
        form.memory.data = desktop.memory
        form.hard_drive.data = desktop.hard_drive
        form.case.data = desktop.case

    return render_template('desktop_detail.html', desktop=desktop, form=form)


@app.route("/product_detail/<int:laptop_id>/laptop", methods=['GET', 'POST'])
def laptop_detail(laptop_id):
    laptop = Laptop.query.get_or_404(laptop_id)
    form = CustomizeLaptopForm()

    form.processor.choices = [processor.name for processor in LaptopProcessor.query.order_by('name')]
    form.graphic_card.choices = [g.name for g in GraphicCard.query.order_by('name')]
    form.memory.choices = [g.spec for g in Memory.query.order_by('spec')]
    form.hard_drive.choices = [g.spec for g in HardDrive.query.order_by('spec')]

    if form.validate_on_submit():
        if current_user.is_customer:
            if current_user.has_discount:
                new_price = (LaptopProcessor.query.filter_by(name=form.processor.data).first().price + 
                    GraphicCard.query.filter_by(name=form.graphic_card.data).first().price +
                    Memory.query.filter_by(spec=form.memory.data).first().price +
                    HardDrive.query.filter_by(spec=form.hard_drive.data).first().price) * Decimal(0.9)
            else:
                new_price = (LaptopProcessor.query.filter_by(name=form.processor.data).first().price + 
                        GraphicCard.query.filter_by(name=form.graphic_card.data).first().price +
                        Memory.query.filter_by(spec=form.memory.data).first().price +
                        HardDrive.query.filter_by(spec=form.hard_drive.data).first().price)
            
            checkout_item = CheckoutItem(item_name=laptop.name, price=new_price, config_id=laptop.id, is_laptop=True)
            db.session.add(checkout_item)
            db.session.commit()
            id = CheckoutItem.query.order_by(CheckoutItem.id.desc()).first().id
            return redirect(url_for('checkout',checkout_id=id))

    elif request.method == 'GET':
        form.processor.data = laptop.processor
        form.graphic_card.data = laptop.graphic_card
        form.memory.data = laptop.memory
        form.hard_drive.data = laptop.hard_drive

    return render_template('laptop_detail.html', laptop=laptop, form=form)


@app.route("/product_detail/<int:edge_computing_id>/edge_computing", methods=['GET', 'POST'])
def edge_computing_detail(edge_computing_id):
    edge_computing = EdgeComputing.query.get_or_404(edge_computing_id)
    form = CustomizeEdgeComputingForm()

    form.RAM.choices = [g.RAM for g in EdgeComputingRAM.query.filter_by(name=edge_computing.name)]

    if form.validate_on_submit():
        if current_user.is_customer:
            if current_user.has_discount:
                new_price = EdgeComputingRAM.query.filter_by(RAM=form.RAM.data).first().price * Decimal(0.9)
            else:
                new_price = EdgeComputingRAM.query.filter_by(RAM=form.RAM.data).first().price

            checkout_item = CheckoutItem(item_name=edge_computing.name, price=new_price, config_id=edge_computing.id,
                                         is_edge_computing=True)
            db.session.add(checkout_item)
            db.session.commit()
            id = CheckoutItem.query.order_by(CheckoutItem.id.desc()).first().id
            return redirect(url_for('checkout',checkout_id=id))
    elif request.method == 'GET':
        form.RAM.data = edge_computing.RAM

    return render_template('edge_computing_detail.html', edge_computing=edge_computing, form=form)
        

@app.route("/product_detail/<int:macbook_id>/macbook", methods=['GET', 'POST'])
def macbook_detail(macbook_id):
    macbook = MacbookAir.query.get_or_404(macbook_id)
    form = CustomizeMacbookForm()

    form.memory.choices = [(g.memory, g.memory) for g in MacbookAirRAM.query.all()]
    form.storage.choices = [(g.hard_drive, g.hard_drive) for g in MacbookAirStorage.query.all()]

    if form.validate_on_submit():
        if current_user.is_customer:
            if current_user.has_discount:
                new_price = (MacbookList.query.filter_by(name=macbook.name).first().price +
                        MacbookAirRAM.query.filter_by(memory=form.memory.data).first().price +
                        MacbookAirStorage.query.filter_by(hard_drive=form.storage.data).first().price) * Decimal(0.9)
            else:
                new_price = (MacbookList.query.filter_by(name=macbook.name).first().price +
                            MacbookAirRAM.query.filter_by(memory=form.memory.data).first().price +
                            MacbookAirStorage.query.filter_by(hard_drive=form.storage.data).first().price)
            checkout_item = CheckoutItem(item_name=macbook.name, price=new_price, config_id=macbook.id, is_macbook=True)
            db.session.add(checkout_item)
            db.session.commit()
            id = CheckoutItem.query.order_by(CheckoutItem.id.desc()).first().id
            return redirect(url_for('checkout',checkout_id=id))
    elif request.method == 'GET':
        form.memory.data = macbook.memory
        form.storage.data = macbook.hard_drive
    
    return render_template('macbook_detail.html', macbook=macbook, form=form)

@app.route("/product_detail/<int:imac_id>/imac", methods=['GET', 'POST'])
def imac_detail(imac_id):
    imac = iMac.query.get_or_404(imac_id)
    form = CustomizeiMacForm()

    form.memory.choices = [(g.memory, g.memory) for g in iMacMemoryList.query.all()]
    form.storage.choices = [(g.hard_drive, g.hard_drive) for g in iMacStoragelist.query.all()]
    form.accessory.choices = [(g.accessory, g.accessory) for g in iMacAccessoryList.query.all()]

    if form.validate_on_submit():
        if current_user.is_customer:
            if current_user.has_discount:
                new_price = (iMacList.query.filter_by(name=imac.name).first().price +
                        iMacAccessoryList.query.filter_by(accessory=form.accessory.data).first().price +
                        iMacStoragelist.query.filter_by(hard_drive=form.storage.data).first().price +
                        iMacMemoryList.query.filter_by(memory=form.memory.data).first().price) * Decimal(0.9)
            else:
                new_price = (iMacList.query.filter_by(name=imac.name).first().price +
                            iMacAccessoryList.query.filter_by(accessory=form.accessory.data).first().price +
                            iMacStoragelist.query.filter_by(hard_drive=form.storage.data).first().price +
                            iMacMemoryList.query.filter_by(memory=form.memory.data).first().price)
            checkout_item = CheckoutItem(item_name=imac.name, price=new_price, config_id=imac.id, is_imac=True)
            db.session.add(checkout_item)
            db.session.commit()
            id = CheckoutItem.query.order_by(CheckoutItem.id.desc()).first().id
            return redirect(url_for('checkout',checkout_id=id))
    elif request.method == 'GET':
        form.color.data = imac.color
        form.memory.data = imac.memory
        form.storage.data = imac.hard_drive
        form.accessory.data = imac.accessory

    return render_template('imac_detail.html', imac=imac, form=form)


def check_comment(comment):
    content_array = comment.split()
    taboo_list = ['fuck','fucking','slut','bitch','dick','fk','fkin','fucker','shit', 'fker', 'suck', 'ass', 'pussy']
    count = 0
    for i in range(len(taboo_list)):
        for j in range(len(content_array)):
            if taboo_list[i] in content_array[j].lower():
                content_array[j] = (content_array[j].lower()).replace(taboo_list[i], '*'*len(taboo_list[i]))
                count += 1
    return [" ".join(content_array), count]
                

def check_warning(user):
    if user.is_customer:
        if user.warning >= 3:
            block_user = UserBlacklist(user_blacklisted_email=user.email)
            User.query.filter_by(email=user.email).first().is_blacklisted = True
            msg = Message('You Are Banned', sender='noreply@demo.com', recipients=[user.email])
            msg.body = f'''Dear {user.name}
            Our online store has zero tolerance on offensive and hateful language. We have warned you, and now decided to ban you from accessing our store. Please consult with store owner/employee for any issue.

            Computer Tech
            '''
            mail.send(msg)
            db.session.add(block_user)
            db.session.commit()
            logout_user()
    elif user.is_employee:
        if user.demote_count >= 2:
            delete_user = User.query.filter_by(email=user.email).first()
            msg = Message('You Are Fired', sender='noreply@demo.com', recipients=[user.email])
            msg.body = f'''Dear {user.name}
            Our online store has zero tolerance on offensive and hateful language. We have warned you, and now decided to remove you from your position as an employee in our store. Hope you find new success in your future career.

            Computer Tech
            '''
            mail.send(msg)
            logout_user()
            db.session.delete(delete_user)
            db.session.commit()
        else:
            if user.warning >= 3:
                user.demote_count += 1
                user.employee_title -= 1
                user.warning -= 3
                db.session.commit()

def check_compliment(user):
    if user.is_customer:
        if user.compliment >= 3:
            user.has_discount = True
            user.compliment -= 3
            db.session.commit()
    elif user.is_employee:
        if user.compliment >= 3:
            if user.demote_count > 0:
                user.demote_count -= 1
            user.employee_title += 1
            user.compliment -= 3
            db.session.commit()


@app.route("/add_desktop_comment/<int:desktop_id>", methods=['GET', 'POST'])
def add_desktop_comment(desktop_id):
    form = AddCommentForm()
    desktop = Desktop.query.get_or_404(desktop_id)
    
    if form.validate_on_submit():
        warning_count = check_comment(form.content.data)[1]
        form.content.data = check_comment(form.content.data)[0]

        if current_user.is_authenticated:
            if warning_count > 0 and warning_count <= 3:
                current_user.warning += 1
                comment = DesktopComment(desktop_id=desktop_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('desktop_comment',desktop_id=desktop_id))
            elif warning_count > 3:
                current_user.warning += 2
                db.session.commit()
                flash('No offensive/hateful language is allowed', 'error')
                check_warning(current_user)
                return redirect(url_for('desktop_comment',desktop_id=desktop_id))
            else:
                comment = DesktopComment(desktop_id=desktop_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('desktop_comment',desktop_id=desktop_id))
        else:
            if warning_count > 0:
                flash('No offensive/hateful language is allowed', 'error')
                return redirect(url_for('desktop_comment',desktop_id=desktop_id))
            else:
                comment = DesktopComment(desktop_id=desktop_id, comment=form.content.data)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                return redirect(url_for('desktop_comment',desktop_id=desktop_id))

    return render_template('add_desktop_comment.html', form=form, legend='New Comment', desktop=desktop)

@app.route("/product_detail/<int:desktop_id>/desktop/comment", methods=['GET','POST'])
def desktop_comment(desktop_id):
    desktop = Desktop.query.get_or_404(desktop_id)
    page = request.args.get('page', 1, type=int)
    comments = DesktopComment.query.filter_by(desktop_id=desktop_id).order_by(DesktopComment.date_submitted.desc()).paginate(page=page, per_page=10)
    return render_template('desktop_comment.html', comments=comments, desktop=desktop)


@app.route("/add_laptop_comment/<int:laptop_id>", methods=['GET', 'POST'])
def add_laptop_comment(laptop_id):
    form = AddCommentForm()
    laptop = Laptop.query.get_or_404(laptop_id)

    if form.validate_on_submit():
        warning_count = check_comment(form.content.data)[1]
        form.content.data = check_comment(form.content.data)[0]

        if current_user.is_authenticated:
            if warning_count > 0 and warning_count <= 3:
                current_user.warning += 1
                comment = LaptopComment(laptop_id=laptop_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('laptop_comment', laptop_id=laptop_id))
            elif warning_count > 3:
                current_user.warning += 2
                db.session.commit()
                flash('No offensive/hateful language is allowed', 'error')
                check_warning(current_user)
                return redirect(url_for('laptop_comment', laptop_id=laptop_id))
            else:
                comment = LaptopComment(laptop_id=laptop_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('laptop_comment',laptop_id=laptop_id))
        else:
            if warning_count > 0:
                flash('No offensive/hateful language is allowed', 'error')
                return redirect(url_for('laptop_comment',laptop_id=laptop_id))
            else:
                comment = LaptopComment(laptop_id=laptop_id, comment=form.content.data)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                return redirect(url_for('laptop_comment',laptop_id=laptop_id))

    return render_template('add_laptop_comment.html', form=form, legend='New Comment', laptop=laptop)

@app.route("/product_detail/<int:laptop_id>/laptop/comment", methods=['GET','POST'])
def laptop_comment(laptop_id):
    laptop = Laptop.query.get_or_404(laptop_id)
    page = request.args.get('page', 1, type=int)
    comments = LaptopComment.query.filter_by(laptop_id=laptop_id).order_by(LaptopComment.date_submitted.desc()).paginate(page=page, per_page=10)
    return render_template('laptop_comment.html', comments=comments, laptop=laptop)

@app.route("/add_edge_computing_comment/<int:edge_computing_id>", methods=['GET', 'POST'])
def add_edge_computing_comment(edge_computing_id):
    form = AddCommentForm()
    edge_computing = EdgeComputing.query.get_or_404(edge_computing_id)

    if form.validate_on_submit():
        warning_count = check_comment(form.content.data)[1]
        form.content.data = check_comment(form.content.data)[0]

        if current_user.is_authenticated:
            if warning_count > 0 and warning_count <= 3:
                current_user.warning += 1
                comment = EdgeComputingComment(edge_computing_id=edge_computing_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('edge_computing_comment', edge_computing_id=edge_computing_id))
            elif warning_count > 3:
                current_user.warning += 2
                db.session.commit()
                flash('No offensive/hateful language is allowed', 'error')
                check_warning(current_user)
                return redirect(url_for('edge_computing_comment', edge_computing_id=edge_computing_id))
            else:
                comment = EdgeComputingComment(edge_computing_id=edge_computing_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('edge_computing_comment',edge_computing_id=edge_computing_id))
        else:
            if warning_count > 0:
                flash('No offensive/hateful language is allowed', 'error')
                return redirect(url_for('edge_computing_comment',edge_computing_id=edge_computing_id))
            else:
                comment = EdgeComputingComment(edge_computing_id=edge_computing_id, comment=form.content.data)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                return redirect(url_for('edge_computing_comment',edge_computing_id=edge_computing_id))

    return render_template('add_edge_computing_comment.html', form=form, legend='New Comment', edge_computing=edge_computing)

@app.route("/product_detail/<int:edge_computing_id>/edge_computing/comment", methods=['GET','POST'])
def edge_computing_comment(edge_computing_id):
    edge_computing = EdgeComputing.query.get_or_404(edge_computing_id)
    page = request.args.get('page', 1, type=int)
    comments = EdgeComputingComment.query.filter_by(edge_computing_id=edge_computing_id).order_by(EdgeComputingComment.date_submitted.desc()).paginate(page=page, per_page=10)
    return render_template('edge_computing_comment.html', comments=comments, edge_computing=edge_computing)

@app.route("/add_macbook_comment/<int:macbook_id>", methods=['GET', 'POST'])
def add_macbook_comment(macbook_id):
    form = AddCommentForm()
    macbook = MacbookAir.query.get_or_404(macbook_id)

    if form.validate_on_submit():
        warning_count = check_comment(form.content.data)[1]
        form.content.data = check_comment(form.content.data)[0]

        if current_user.is_authenticated:
            if warning_count > 0 and warning_count <= 3:
                current_user.warning += 1
                comment = MacbookComment(macbook_id=macbook_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('macbook_comment', macbook_id=macbook_id))
            elif warning_count > 3:
                current_user.warning += 2
                db.session.commit()
                flash('No offensive/hateful language is allowed', 'error')
                check_warning(current_user)
                return redirect(url_for('macbook_comment', macbook_id=macbook_id))
            else:
                comment = MacbookComment(macbook_id=macbook_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('macbook_comment',macbook_id=macbook_id))
        else:
            if warning_count > 0:
                flash('No offensive/hateful language is allowed', 'error')
                return redirect(url_for('macbook_comment',macbook_id=macbook_id))
            else:
                comment = MacbookComment(macbook_id=macbook_id, comment=form.content.data)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                return redirect(url_for('macbook_comment',macbook_id=macbook_id))

    return render_template('add_macbook_comment.html', form=form, legend='New Comment', macbook=macbook)

@app.route("/product_detail/<int:macbook_id>/macbook/comment", methods=['GET','POST'])
def macbook_comment(macbook_id):
    macbook = MacbookAir.query.get_or_404(macbook_id)
    page = request.args.get('page', 1, type=int)
    comments = MacbookComment.query.filter_by(macbook_id=macbook_id).order_by(MacbookComment.date_submitted.desc()).paginate(page=page, per_page=10)
    return render_template('macbook_comment.html', comments=comments, macbook=macbook)

@app.route("/add_imac_comment/<int:imac_id>", methods=['GET', 'POST'])
def add_imac_comment(imac_id):
    form = AddCommentForm()
    imac = iMac.query.get_or_404(imac_id)

    if form.validate_on_submit():
        warning_count = check_comment(form.content.data)[1]
        form.content.data = check_comment(form.content.data)[0]

        if current_user.is_authenticated:
            if warning_count > 0 and warning_count <= 3:
                current_user.warning += 1
                comment = iMacComment(imac_id=imac_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('imac_comment', imac_id=imac_id))
            elif warning_count > 3:
                current_user.warning += 2
                db.session.commit()
                flash('No offensive/hateful language is allowed', 'error')
                check_warning(current_user)
                return redirect(url_for('imac_comment', imac_id=imac_id))
            else:
                comment = iMacComment(imac_id=imac_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('imac_comment',imac_id=imac_id))
        else:
            if warning_count > 0:
                flash('No offensive/hateful language is allowed', 'error')
                return redirect(url_for('imac_comment',imac_id=imac_id))
            else:
                comment = iMacComment(imac_id=imac_id, comment=form.content.data)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                return redirect(url_for('imac_comment',imac_id=imac_id))

    return render_template('add_imac_comment.html', form=form, legend='New Comment', imac=imac)

@app.route("/product_detail/<int:imac_id>/imac/comment", methods=['GET','POST'])
def imac_comment(imac_id):
    imac = iMac.query.get_or_404(imac_id)
    page = request.args.get('page', 1, type=int)
    comments = iMacComment.query.filter_by(imac_id=imac_id).order_by(iMacComment.date_submitted.desc()).paginate(page=page, per_page=10)
    return render_template('imac_comment.html', comments=comments, imac=imac)


@app.route("/communicate", methods=['GET', 'POST'])
@login_required
def communicate():
    if current_user.is_customer:
        page = request.args.get('page', 1, type=int)
        communicates = Communicate.query.filter_by(user_id=current_user.id).order_by(Communicate.date_submitted.desc()).paginate(page=page, per_page=10)
        return render_template('customer_communicate.html', communicates=communicates)
    
    elif current_user.is_employee:
        page = request.args.get('page', 1, type=int)
        communicates = Communicate.query.order_by(Communicate.date_submitted.desc()).paginate(page=page, per_page=10)
        return render_template('employee_communicate.html', communicates=communicates)
    
@app.route("/communicate/new", methods=['GET','POST'])
@login_required
def new_communicate():
    if current_user.is_customer:
        form = NewCommunicateForm()

        if form.validate_on_submit():
            warning_count = check_comment(form.title.data)[1]
            form.title.data = check_comment(form.title.data)[0]

            if not CheckoutItem.query.filter_by(id=form.order_id.data).first():
                flash('No existing order with this Order ID', 'error')
                return redirect(url_for('new_communicate'))

            is_order_valid = CheckoutItem.query.filter_by(id=form.order_id.data).first().is_checkedout

            if is_order_valid:
                if warning_count > 3:
                    current_user.warning += 2
                    db.session.commit()
                    flash('No offensive/hateful language is allowed', 'error')
                    check_warning(current_user)
                    return redirect(url_for('new_communicate'))
                elif warning_count > 0 and warning_count <= 3:
                    current_user.warning += 1
                    communicate = Communicate(order_id=form.order_id.data, title=form.title.data, author=current_user.name,
                                            user_id=current_user.id)
                    db.session.add(communicate)
                    db.session.commit()
                    order_id = Communicate.query.order_by(Communicate.id.desc()).first().order_id
                    flash('Your Request Has Been Sent, Please Add More Description To Address Your Problem/Concern', 'success')
                    check_warning(current_user)
                    return redirect(url_for('add_reply', order_id=order_id))
                else:
                    communicate = Communicate(order_id=form.order_id.data, title=form.title.data, author=current_user.name,
                                            user_id=current_user.id)
                    db.session.add(communicate)
                    db.session.commit()
                    order_id = Communicate.query.order_by(Communicate.id.desc()).first().order_id
                    flash('Your Request Has Been Sent, Please Add More Description To Address Your Problem/Concern', 'success')
                    check_warning(current_user)
                    return redirect(url_for('add_reply', order_id=order_id))
            else:
                flash('No existing order with this Order ID', 'error')
                return redirect(url_for('new_communicate'))
        
        return render_template('new_communicate.html', form=form)
    
@app.route("/communicate/add_reply/<int:order_id>", methods=['GET','POST'])
@login_required
def add_reply(order_id):
    form = CommunicateCommentForm()

    if form.validate_on_submit():
        warning_count = check_comment(form.content.data)[1]
        form.content.data = check_comment(form.content.data)[0]

        if warning_count > 3:
            current_user.warning += 2
            db.session.commit()
            flash('No offensive/hateful language is allowed', 'error')
            check_warning(current_user)
            return redirect(url_for('add_reply', order_id=order_id))
        elif warning_count > 0 and warning_count <= 3:
            current_user.warning += 1
            reply = CommunicateComment(user_id=current_user.id, order_id=order_id, image_file=current_user.image_file,
                                    author=current_user.name, content=form.content.data)
            db.session.add(reply)
            db.session.commit()
            flash('Reply Added', 'success')
            check_warning(current_user)
            return redirect(url_for('communicate_detail', order_id=order_id))
        else:
            reply = CommunicateComment(user_id=current_user.id, order_id=order_id, image_file=current_user.image_file,
                                    author=current_user.name, content=form.content.data)
            db.session.add(reply)
            db.session.commit()
            flash('Reply Added', 'success')
            check_warning(current_user)
            return redirect(url_for('communicate_detail', order_id=order_id))
    
    return render_template('add_reply.html', form=form, order_id=order_id)


@app.route("/communicate/communicate_detail/report_to_admin",methods=['GET','POST'])
@login_required
def report_admin():
    if current_user.is_customer or current_user.is_employee:
        form = ContactAdminForm()
        if form.validate_on_submit():
            warning_count = check_comment(form.content.data)[1]

            if warning_count > 0:
                flash('No offensive/hateful language is allowed', 'error')
                return redirect(url_for('report_admin'))
            else:
                report = Reports(reporter_id=current_user.id, reported_user_id=form.reported_user_id.data,content=form.content.data)
                db.session.add(report)
                db.session.commit()
                flash('Your Report Has Been Submitted', 'success')
                return redirect(url_for('communicate'))
        return render_template('report_admin.html', form=form)


@app.route("/communicate/communicate_detail/<int:order_id>", methods=['GET','POST'])
@login_required
def communicate_detail(order_id):
    page = request.args.get('page', 1, type=int)
    replies = CommunicateComment.query.filter_by(order_id=order_id).order_by(CommunicateComment.date_submitted).paginate(page=page, per_page=10)
    return render_template('communicate_detail.html', order_id=order_id, replies=replies)
            
@app.route("/reports", methods=['GET','POST'])
@login_required
def reports():
    if current_user.is_admin:
        page = request.args.get('page', 1, type=int)
        reports = Reports.query.order_by(Reports.date_submitted.desc()).paginate(page=page, per_page=10)
        return render_template('reports.html', reports=reports)

@app.route("/reports/<int:report_id>", methods=['GET','POST'])
@login_required
def process_report(report_id):
    if current_user.is_admin:
        form = ProcessReportForm()
        if form.validate_on_submit():
            reported_user_id = Reports.query.filter_by(id=report_id).first().reported_user_id
            report = Reports.query.filter_by(id=report_id).first()
            reported_user = User.query.filter_by(id=reported_user_id).first()
            reported_user.compliment += form.compliment.data
            reported_user.warning += form.warning.data
            db.session.delete(report)
            db.session.commit()
            check_warning(reported_user)
            check_compliment(reported_user)
            flash('Report has been processed', 'success')
            return redirect(url_for('reports'))
        return render_template('process_report.html', report_id=report_id, form=form)

@app.route("/build_desktop",methods=['GET','POST'])
@login_required
def build_desktop():
    if current_user.is_customer:
        form = AddDesktopForm()
        # Populate all choices first
        form.motherboard.choices = [None]+[g.name for g in Motherboard.query.all()]
        form.processor.choices = [(processor.name, processor.name) for processor in Processor.query.all()]
        form.graphic_card.choices = [g.name for g in GraphicCard.query.order_by('name')]
        form.memory.choices = [g.spec for g in Memory.query.order_by('spec')]
        form.hard_drive.choices = [g.spec for g in HardDrive.query.order_by('spec')]
        form.case.choices = [g.name for g in Case.query.order_by('name')]

        if form.validate_on_submit():
            if current_user.has_discount:
                price = (Processor.query.filter_by(name=form.processor.data).first().price + 
                    GraphicCard.query.filter_by(name=form.graphic_card.data).first().price +
                    Memory.query.filter_by(spec=form.memory.data).first().price +
                    HardDrive.query.filter_by(spec=form.hard_drive.data).first().price +
                    Motherboard.query.filter_by(name=form.motherboard.data).first().price +
                    Case.query.filter_by(name=form.case.data).first().price) * Decimal(0.9)
            else:
                price = (Processor.query.filter_by(name=form.processor.data).first().price + 
                        GraphicCard.query.filter_by(name=form.graphic_card.data).first().price +
                        Memory.query.filter_by(spec=form.memory.data).first().price +
                        HardDrive.query.filter_by(spec=form.hard_drive.data).first().price +
                        Motherboard.query.filter_by(name=form.motherboard.data).first().price +
                        Case.query.filter_by(name=form.case.data).first().price)
            
            desktop = CustomerMadeDesktop(name=form.name.data, processor=form.processor.data, graphic_card=form.graphic_card.data,
                                operating_system=form.operating_system.data, memory=form.memory.data, hard_drive=form.hard_drive.data,
                                motherboard=form.motherboard.data, case=form.case.data, category=form.category.data,
                                price=price,
                                    image_file=Case.query.filter_by(name=form.case.data).first().image_file,
                                    creator_id=current_user.id)
            db.session.add(desktop)
            checkout_item = CheckoutItem(item_name=form.name.data, price=price, madeby_customer=True)
            db.session.add(checkout_item)
            db.session.commit()
            id = CheckoutItem.query.order_by(CheckoutItem.id.desc()).first().id
            return redirect(url_for('checkout',checkout_id=id))
            
        return render_template('build_desktop.html', form=form)
    
@app.route("/display_permission", methods=['GET','POST'])
@login_required
def display_permission():
    if current_user.is_customer:
        form = DisplayPermissionForm()

        if form.validate_on_submit():
            if form.allow.data == 'Yes':
                CustomerMadeDesktop.query.filter_by(creator_id=current_user.id).order_by(CustomerMadeDesktop.id.desc()).first().allow_for_display = True
                db.session.commit()
            else:
                pass
            return redirect(url_for('home'))
        return render_template('display_permission.html', form=form)
    
@app.route("/add_customer_made_desktop_comment/<int:desktop_id>", methods=['GET', 'POST'])
def add_customer_made_desktop_comment(desktop_id):
    form = AddCommentForm()
    desktop = CustomerMadeDesktop.query.get_or_404(desktop_id)
    
    if form.validate_on_submit():
        warning_count = check_comment(form.content.data)[1]
        form.content.data = check_comment(form.content.data)[0]

        if current_user.is_authenticated:
            if warning_count > 0 and warning_count <= 3:
                current_user.warning += 1
                comment = CustomerMadeDesktopComment(desktop_id=desktop_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('customer_made_desktop_comment',desktop_id=desktop_id))
            elif warning_count > 3:
                current_user.warning += 2
                db.session.commit()
                flash('No offensive/hateful language is allowed', 'error')
                check_warning(current_user)
                return redirect(url_for('customer_made_desktop_comment',desktop_id=desktop_id))
            else:
                comment = CustomerMadeDesktopComment(desktop_id=desktop_id, author=current_user.name, comment=form.content.data,
                                     image_file=current_user.image_file)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                check_warning(current_user)
                return redirect(url_for('customer_made_desktop_comment',desktop_id=desktop_id))
        else:
            if warning_count > 0:
                flash('No offensive/hateful language is allowed', 'error')
                return redirect(url_for('customer_made_desktop_comment',desktop_id=desktop_id))
            else:
                comment = CustomerMadeDesktopComment(desktop_id=desktop_id, comment=form.content.data)
                db.session.add(comment)
                db.session.commit()
                flash('Comment Added', 'success')
                return redirect(url_for('customer_made_desktop_comment',desktop_id=desktop_id))

    return render_template('add_customer_made_desktop_comment.html', form=form, legend='New Comment', desktop=desktop)

@app.route("/product_detail/<int:desktop_id>/customer_made_desktop/comment", methods=['GET','POST'])
def customer_made_desktop_comment(desktop_id):
    desktop = CustomerMadeDesktop.query.get_or_404(desktop_id)
    page = request.args.get('page', 1, type=int)
    comments = CustomerMadeDesktopComment.query.filter_by(desktop_id=desktop_id).order_by(CustomerMadeDesktopComment.date_submitted.desc()).paginate(page=page, per_page=10)
    return render_template('customer_made_desktop_comment.html', comments=comments, desktop=desktop)

@app.route("/product_detail/<int:desktop_id>/customer_desktop", methods=['POST','GET'])
def customer_desktop_detail(desktop_id):
    desktop = CustomerMadeDesktop.query.get_or_404(desktop_id)
    form = CustomizeDesktopForm()

    form.motherboard.choices = [None]+[g.name for g in Motherboard.query.all()]
    form.processor.choices = [(processor.name, processor.name) for processor in Processor.query.all()]
    form.graphic_card.choices = [g.name for g in GraphicCard.query.order_by('name')]
    form.memory.choices = [g.spec for g in Memory.query.order_by('spec')]
    form.hard_drive.choices = [g.spec for g in HardDrive.query.order_by('spec')]
    form.case.choices = [g.name for g in Case.query.order_by('name')]

    if form.validate_on_submit():    
        if current_user.is_authenticated and current_user.is_customer:
            if current_user.has_discount:
                new_price = (Processor.query.filter_by(name=form.processor.data).first().price + 
                    GraphicCard.query.filter_by(name=form.graphic_card.data).first().price +
                    Memory.query.filter_by(spec=form.memory.data).first().price +
                    HardDrive.query.filter_by(spec=form.hard_drive.data).first().price +
                    Motherboard.query.filter_by(name=form.motherboard.data).first().price +
                    Case.query.filter_by(name=form.case.data).first().price) * Decimal(0.9)
            else:
                new_price = (Processor.query.filter_by(name=form.processor.data).first().price + 
                        GraphicCard.query.filter_by(name=form.graphic_card.data).first().price +
                        Memory.query.filter_by(spec=form.memory.data).first().price +
                        HardDrive.query.filter_by(spec=form.hard_drive.data).first().price +
                        Motherboard.query.filter_by(name=form.motherboard.data).first().price +
                        Case.query.filter_by(name=form.case.data).first().price)
            
            checkout_item = CheckoutItem(item_name=desktop.name, price=new_price, config_id=desktop.id, is_customer_desktop=True)
            db.session.add(checkout_item)
            db.session.commit()
            id = CheckoutItem.query.order_by(CheckoutItem.id.desc()).first().id
            return redirect(url_for('checkout',checkout_id=id))

    elif request.method == 'GET':
        form.motherboard.data = desktop.motherboard
        form.processor.data = desktop.processor
        form.graphic_card.data = desktop.graphic_card
        form.memory.data = desktop.memory
        form.hard_drive.data = desktop.hard_drive
        form.case.data = desktop.case

    return render_template('customer_desktop_detail.html', desktop=desktop, form=form)

@app.route("/delete_customer_desktop/<int:desktop_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_customer_desktop(desktop_id):
    if current_user.is_employee:
        desktop = CustomerMadeDesktop.query.get_or_404(desktop_id)
        comments = CustomerMadeDesktopComment.query.filter_by(desktop_id=desktop_id).all()
        for i in comments:
            db.session.delete(i)
        db.session.delete(desktop)
        db.session.commit()
        flash('Desktop Deleted', 'success')
        return redirect(url_for('home'))
    
def check_configuration(config):
    if config.rating_5 > 3 and config.rating_1 == 0:
        creator = User.query.filter_by(id=config.creator_id).first()
        creator.compliment += 1
        db.session.commit()
        check_compliment(creator)
    elif config.rating_1 > 3 and config.rating_5 == 0:
        creator = User.query.filter_by(id=config.creator_id).first()
        creator.warning += 1
        db.session.delete(config)
        db.session.commit()
        check_warning(creator)

@app.route("/rate_desktop_configuration/<int:desktop_id>", methods=['GET','POST'])
@login_required
def rate_desktop_configuration(desktop_id):
    if current_user.is_customer:
        form = RatingForm()
        if form.validate_on_submit():
            desktop = Desktop.query.filter_by(id=desktop_id).first()
            if form.rating.data == '1':
                desktop.rating_1 += 1
                db.session.commit()
            elif form.rating.data == '2':
                desktop.rating_2 += 1
                db.session.commit()
            elif form.rating.data == '3':
                desktop.rating_3 += 1
                db.session.commit()
            elif form.rating.data == '4':
                desktop.rating_4 += 1
                db.session.commit()
            else:
                desktop.rating_5 += 1
                db.session.commit()
            check_configuration(desktop)
            return redirect(url_for('home'))
        return render_template('rate_desktop_configuration.html', desktop_id=desktop_id, form=form)

@app.route("/rate_laptop_configuration/<int:laptop_id>", methods=['GET','POST'])
@login_required
def rate_laptop_configuration(laptop_id):
    if current_user.is_customer:
        form = RatingForm()
        if form.validate_on_submit():
            laptop = Laptop.query.filter_by(id=laptop_id).first()
            if form.rating.data == '1':
                laptop.rating_1 += 1
                db.session.commit()
            elif form.rating.data == '2':
                laptop.rating_2 += 1
                db.session.commit()
            elif form.rating.data == '3':
                laptop.rating_3 += 1
                db.session.commit()
            elif form.rating.data == '4':
                laptop.rating_4 += 1
                db.session.commit()
            else:
                laptop.rating_5 += 1
                db.session.commit()
            check_configuration(laptop)
            return redirect(url_for('home'))
        return render_template('rate_laptop_configuration.html', laptop_id=laptop_id, form=form)
    
@app.route("/rate_macbook_configuration/<int:macbook_id>", methods=['GET','POST'])
@login_required
def rate_macbook_configuration(macbook_id):
    if current_user.is_customer:
        form = RatingForm()
        if form.validate_on_submit():
            macbook = MacbookAir.query.filter_by(id=macbook_id).first()
            if form.rating.data == '1':
                macbook.rating_1 += 1
                db.session.commit()
            elif form.rating.data == '2':
                macbook.rating_2 += 1
                db.session.commit()
            elif form.rating.data == '3':
                macbook.rating_3 += 1
                db.session.commit()
            elif form.rating.data == '4':
                macbook.rating_4 += 1
                db.session.commit()
            else:
                macbook.rating_5 += 1
                db.session.commit()
            check_configuration(macbook)
            return redirect(url_for('home'))
        return render_template('rate_macbook_configuration.html', macbook_id=macbook_id, form=form)
    
@app.route("/rate_imac_configuration/<int:imac_id>", methods=['GET','POST'])
@login_required
def rate_imac_configuration(imac_id):
    if current_user.is_customer:
        form = RatingForm()
        if form.validate_on_submit():
            imac = iMac.query.filter_by(id=imac_id).first()
            if form.rating.data == '1':
                imac.rating_1 += 1
                db.session.commit()
            elif form.rating.data == '2':
                imac.rating_2 += 1
                db.session.commit()
            elif form.rating.data == '3':
                imac.rating_3 += 1
                db.session.commit()
            elif form.rating.data == '4':
                imac.rating_4 += 1
                db.session.commit()
            else:
                imac.rating_5 += 1
                db.session.commit()
            check_configuration(imac)
            return redirect(url_for('home'))
        return render_template('rate_imac_configuration.html', imac_id=imac_id, form=form)
    
@app.route("/rate_edge_computing_configuration/<int:edge_computing_id>", methods=['GET','POST'])
@login_required
def rate_edge_computing_configuration(edge_computing_id):
    if current_user.is_customer:
        form = RatingForm()
        if form.validate_on_submit():
            edge_computing = EdgeComputing.query.filter_by(id=edge_computing_id).first()
            if form.rating.data == '1':
                edge_computing.rating_1 += 1
                db.session.commit()
            elif form.rating.data == '2':
                edge_computing.rating_2 += 1
                db.session.commit()
            elif form.rating.data == '3':
                edge_computing.rating_3 += 1
                db.session.commit()
            elif form.rating.data == '4':
                edge_computing.rating_4 += 1
                db.session.commit()
            else:
                edge_computing.rating_5 += 1
                db.session.commit()
            check_configuration(edge_computing)
            return redirect(url_for('home'))
        return render_template('rate_edge_computing_configuration.html', edge_computing_id=edge_computing_id, form=form)
    
@app.route("/rate_customer_desktop_configuration/<int:desktop_id>", methods=['GET','POST'])
@login_required
def rate_customer_desktop_configuration(desktop_id):
    if current_user.is_customer:
        form = RatingForm()
        if form.validate_on_submit():
            desktop = CustomerMadeDesktop.query.filter_by(id=desktop_id).first()
            if form.rating.data == '1':
                desktop.rating_1 += 1
                db.session.commit()
            elif form.rating.data == '2':
                desktop.rating_2 += 1
                db.session.commit()
            elif form.rating.data == '3':
                desktop.rating_3 += 1
                db.session.commit()
            elif form.rating.data == '4':
                desktop.rating_4 += 1
                db.session.commit()
            else:
                desktop.rating_5 += 1
                db.session.commit()
            check_configuration(desktop)
            return redirect(url_for('home'))
        return render_template('rate_customer_desktop_configuration.html', desktop_id=desktop_id, form=form)
    
