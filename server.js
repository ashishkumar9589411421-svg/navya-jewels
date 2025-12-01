const express = require("express");
const path = require("path");
const fs = require("fs");
const bcrypt = require("bcryptjs");
const bodyParser = require("body-parser");
const session = require("express-session");
const expressLayouts = require("express-ejs-layouts");

const app = express();

// === Basic setup ===
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(expressLayouts);
app.set("layout", "layout");

app.use(express.static(path.join(__dirname, "public")));
app.use(bodyParser.urlencoded({ extended: true }));

app.use(
  session({
    secret: "navya_jewels_secret_key",
    resave: false,
    saveUninitialized: false,
  })
);

// === Simple JSON "database" helpers ===
const DATA_DIR = path.join(__dirname, "data");
const USERS_FILE = path.join(DATA_DIR, "users.json");
const PRODUCTS_FILE = path.join(DATA_DIR, "products.json");
const ORDERS_FILE = path.join(DATA_DIR, "orders.json");
const CONTACTS_FILE = path.join(DATA_DIR, "contacts.json");

function ensureDataFiles() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR);
  if (!fs.existsSync(USERS_FILE)) fs.writeFileSync(USERS_FILE, "[]");
  if (!fs.existsSync(PRODUCTS_FILE)) fs.writeFileSync(PRODUCTS_FILE, "[]");
  if (!fs.existsSync(ORDERS_FILE)) fs.writeFileSync(ORDERS_FILE, "[]");
  if (!fs.existsSync(CONTACTS_FILE)) fs.writeFileSync(CONTACTS_FILE, "[]");
}

function readJson(filePath) {
  try {
    const raw = fs.readFileSync(filePath, "utf8");
    return JSON.parse(raw || "[]");
  } catch (e) {
    return [];
  }
}

function writeJson(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

// === Seed products if empty (now with metal + carat + images) ===
function seedProducts() {
  const products = readJson(PRODUCTS_FILE);
  if (products.length === 0) {
    const sample = [
      // GOLD
      {
        id: "G24N001",
        name: "24K Royal Heritage Necklace",
        price: 54999,
        image: "/images/gold-necklace-24k.jpg",
        category: "Necklace",
        metal: "Gold",
        carat: 24,
        description: "Pure 24K gold-inspired finish necklace with intricate heritage motifs, perfect for bridal looks.",
      },
      {
        id: "G22S001",
        name: "22K Temple Set with Earrings",
        price: 42999,
        image: "/images/gold-set-22k.jpg",
        category: "Bridal Set",
        metal: "Gold",
        carat: 22,
        description: "Traditional 22K look choker set with matching jhumkas, inspired by South Indian temple jewelry.",
      },
      {
        id: "G22B001",
        name: "22K Classic Kada Bangle",
        price: 18999,
        image: "/images/gold-bangle-22k.jpg",
        category: "Bangle",
        metal: "Gold",
        carat: 22,
        description: "Elegant single kada with a timeless design, perfect for everyday luxury.",
      },
      {
        id: "G18R001",
        name: "18K Solitaire Style Ring",
        price: 12999,
        image: "/images/gold-ring-18k.jpg",
        category: "Ring",
        metal: "Gold",
        carat: 18,
        description: "Delicate 18K look ring with high-shine stone setting, ideal for proposals and anniversaries.",
      },

      // DIAMOND
      {
        id: "D18R001",
        name: "Diamond Halo Engagement Ring",
        price: 69999,
        image: "/images/diamond-ring-18k.jpg",
        category: "Ring",
        metal: "Diamond",
        carat: 18,
        description: "Sparkling halo diamond style ring set on 18K finish band for a classic proposal moment.",
      },
      {
        id: "D18N001",
        name: "Diamond Droplet Necklace",
        price: 89999,
        image: "/images/diamond-necklace-18k.jpg",
        category: "Necklace",
        metal: "Diamond",
        carat: 18,
        description: "Fine necklace with droplet diamonds-style arrangement that beautifully frames the neckline.",
      },

      // SILVER
      {
        id: "S925B001",
        name: "925 Silver Minimal Bracelet",
        price: 2999,
        image: "/images/silver-bracelet-925.jpg",
        category: "Bracelet",
        metal: "Silver",
        carat: 925, // purity style
        description: "Everyday wear 925 silver bracelet with minimal design for subtle elegance.",
      },
      {
        id: "S925A001",
        name: "925 Silver Anklet with Ghungroo",
        price: 2499,
        image: "/images/silver-anklet-925.jpg",
        category: "Anklet",
        metal: "Silver",
        carat: 925,
        description: "Traditional silver anklet with tiny ghungroos for a soft, melodious charm.",
      },
    ];
    writeJson(PRODUCTS_FILE, sample);
  }
}

ensureDataFiles();
seedProducts();

// === Middleware: share user & cart to all views ===
app.use((req, res, next) => {
  res.locals.currentUser = req.session.user || null;
  res.locals.cart = req.session.cart || [];
  next();
});

// === Helper: auth check ===
function requireLogin(req, res, next) {
  if (!req.session.user) {
    return res.redirect("/login");
  }
  next();
}

// === Routes ===

// Home page
app.get("/", (req, res) => {
  const products = readJson(PRODUCTS_FILE);
  const featured = products.slice(0, 4);
  res.render("index", { pageTitle: "Home", featured });
});

// Shop (all products)
app.get("/shop", (req, res) => {
  const products = readJson(PRODUCTS_FILE);
  res.render("shop", { pageTitle: "All Collections", products });
});

// Gold items page with carat filter
app.get("/gold", (req, res) => {
  const products = readJson(PRODUCTS_FILE);
  const purity = parseInt(req.query.carat || "0", 10); // 0 = all
  let list = products.filter((p) => p.metal === "Gold");

  if (purity) {
    list = list.filter((p) => p.carat === purity);
  }

  res.render("metal-list", {
    pageTitle: "Gold Jewellery",
    heading: "Gold Collection",
    subtitle: "Explore 24K, 22K and 18K inspired gold designs crafted for every occasion.",
    metal: "Gold",
    caratFilter: purity,
    products: list,
  });
});

// Silver items page
app.get("/silver", (req, res) => {
  const products = readJson(PRODUCTS_FILE);
  const purity = parseInt(req.query.carat || "0", 10); // 0 = all
  let list = products.filter((p) => p.metal === "Silver");

  if (purity) {
    list = list.filter((p) => p.carat === purity);
  }

  res.render("metal-list", {
    pageTitle: "Silver Jewellery",
    heading: "Silver Collection",
    subtitle: "Soft, versatile silver pieces for daily wear and gifting.",
    metal: "Silver",
    caratFilter: purity,
    products: list,
  });
});

// Diamond items page
app.get("/diamond", (req, res) => {
  const products = readJson(PRODUCTS_FILE);
  const purity = parseInt(req.query.carat || "0", 10); // 0 = all
  let list = products.filter((p) => p.metal === "Diamond");

  if (purity) {
    list = list.filter((p) => p.carat === purity);
  }

  res.render("metal-list", {
    pageTitle: "Diamond Jewellery",
    heading: "Diamond Collection",
    subtitle: "Shimmering diamond-inspired designs to mark your milestones.",
    metal: "Diamond",
    caratFilter: purity,
    products: list,
  });
});

// Product detail
app.get("/product/:id", (req, res) => {
  const products = readJson(PRODUCTS_FILE);
  const product = products.find((p) => p.id === req.params.id);
  if (!product) {
    return res.status(404).send("Product not found");
  }
  res.render("product", { pageTitle: product.name, product });
});

// Cart - view
app.get("/cart", (req, res) => {
  const products = readJson(PRODUCTS_FILE);
  const cart = req.session.cart || [];
  const detailedCart = cart
    .map((item) => {
      const product = products.find((p) => p.id === item.productId);
      if (!product) return null;
      return {
        product,
        quantity: item.quantity,
        lineTotal: product.price * item.quantity,
      };
    })
    .filter(Boolean);

  const total = detailedCart.reduce((sum, item) => sum + item.lineTotal, 0);
  res.render("cart", { pageTitle: "Cart", cartItems: detailedCart, total });
});

// Cart - add
app.post("/cart/add/:id", (req, res) => {
  const productId = req.params.id;
  const qty = parseInt(req.body.quantity || "1", 10);

  if (!req.session.cart) req.session.cart = [];
  const existing = req.session.cart.find((item) => item.productId === productId);
  if (existing) {
    existing.quantity += qty;
  } else {
    req.session.cart.push({ productId, quantity: qty });
  }

  res.redirect("/cart");
});

// Cart - remove
app.post("/cart/remove/:id", (req, res) => {
  const productId = req.params.id;
  req.session.cart = (req.session.cart || []).filter(
    (item) => item.productId !== productId
  );
  res.redirect("/cart");
});

// Cart - update quantities
app.post("/cart/update", (req, res) => {
  const quantities = req.body.quantity || {};
  if (!req.session.cart) req.session.cart = [];
  req.session.cart.forEach((item) => {
    if (quantities[item.productId]) {
      const newQty = parseInt(quantities[item.productId], 10);
      item.quantity = newQty > 0 ? newQty : 1;
    }
  });
  res.redirect("/cart");
});

// === Authentication ===

// Register page
app.get("/register", (req, res) => {
  res.render("auth-register", { pageTitle: "Sign Up", error: null });
});

// Register handler
app.post("/register", async (req, res) => {
  const { name, email, phone, password } = req.body;

  if (!name || (!email && !phone) || !password) {
    return res.render("auth-register", {
      pageTitle: "Sign Up",
      error: "Please fill all required fields.",
    });
  }

  const users = readJson(USERS_FILE);

  // Check existing by email or phone
  const existing = users.find(
    (u) => (email && u.email === email) || (phone && u.phone === phone)
  );
  if (existing) {
    return res.render("auth-register", {
      pageTitle: "Sign Up",
      error: "User with this email or phone already exists.",
    });
  }

  const hashed = await bcrypt.hash(password, 10);
  const newUser = {
    id: "U" + Date.now(),
    name,
    email: email || null,
    phone: phone || null,
    password: hashed,
  };
  users.push(newUser);
  writeJson(USERS_FILE, users);

  req.session.user = {
    id: newUser.id,
    name: newUser.name,
    email: newUser.email,
    phone: newUser.phone,
  };
  res.redirect("/");
});

// Login page
app.get("/login", (req, res) => {
  res.render("auth-login", { pageTitle: "Login", error: null });
});

// Login handler (email OR phone + password)
app.post("/login", async (req, res) => {
  const { identifier, password } = req.body; // identifier can be email or phone

  if (!identifier || !password) {
    return res.render("auth-login", {
      pageTitle: "Login",
      error: "Please enter your email/phone and password.",
    });
  }

  const users = readJson(USERS_FILE);

  const user = users.find(
    (u) => u.email === identifier || u.phone === identifier
  );

  if (!user) {
    return res.render("auth-login", {
      pageTitle: "Login",
      error: "User not found.",
    });
  }

  const match = await bcrypt.compare(password, user.password);
  if (!match) {
    return res.render("auth-login", {
      pageTitle: "Login",
      error: "Incorrect password.",
    });
  }

  req.session.user = {
    id: user.id,
    name: user.name,
    email: user.email,
    phone: user.phone,
  };

  res.redirect("/");
});

// Logout
app.get("/logout", (req, res) => {
  req.session.destroy(() => {
    res.redirect("/");
  });
});

// === Checkout & Orders ===

// Checkout page
app.get("/checkout", requireLogin, (req, res) => {
  const products = readJson(PRODUCTS_FILE);
  const cart = req.session.cart || [];
  if (cart.length === 0) {
    return res.redirect("/cart");
  }

  const detailedCart = cart
    .map((item) => {
      const product = products.find((p) => p.id === item.productId);
      if (!product) return null;
      return {
        product,
        quantity: item.quantity,
        lineTotal: product.price * item.quantity,
      };
    })
    .filter(Boolean);

  const total = detailedCart.reduce((sum, item) => sum + item.lineTotal, 0);
  res.render("checkout", {
    pageTitle: "Checkout",
    cartItems: detailedCart,
    total,
    error: null,
  });
});

// Checkout submit
app.post("/checkout", requireLogin, (req, res) => {
  const { name, phone, address, city, pincode, paymentMethod } = req.body;
  const products = readJson(PRODUCTS_FILE);
  const cart = req.session.cart || [];

  if (!name || !phone || !address || !city || !pincode || !paymentMethod) {
    const detailedCart = cart
      .map((item) => {
        const product = products.find((p) => p.id === item.productId);
        if (!product) return null;
        return {
          product,
          quantity: item.quantity,
          lineTotal: product.price * item.quantity,
        };
      })
      .filter(Boolean);
    const total = detailedCart.reduce((sum, item) => sum + item.lineTotal, 0);
    return res.render("checkout", {
      pageTitle: "Checkout",
      cartItems: detailedCart,
      total,
      error: "Please fill all fields.",
    });
  }

  const detailedCart = cart
    .map((item) => {
      const product = products.find((p) => p.id === item.productId);
      if (!product) return null;
      return {
        productId: product.id,
        name: product.name,
        price: product.price,
        quantity: item.quantity,
      };
    })
    .filter(Boolean);

  const total = detailedCart.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  const orders = readJson(ORDERS_FILE);
  const newOrder = {
    id: "O" + Date.now(),
    userId: req.session.user.id,
    customerName: name,
    phone,
    address,
    city,
    pincode,
    paymentMethod,
    items: detailedCart,
    total,
    status: "Pending",
    createdAt: new Date().toISOString(),
  };
  orders.push(newOrder);
  writeJson(ORDERS_FILE, orders);

  req.session.cart = []; // clear cart
  res.redirect("/orders");
});

// View user's orders
app.get("/orders", requireLogin, (req, res) => {
  const orders = readJson(ORDERS_FILE).filter(
    (o) => o.userId === req.session.user.id
  );
  res.render("orders", { pageTitle: "My Orders", orders });
});

// === Contact & About ===

app.get("/contact", (req, res) => {
  res.render("contact", { pageTitle: "Contact", success: null, error: null });
});

app.post("/contact", (req, res) => {
  const { name, email, phone, message } = req.body;
  if (!name || (!email && !phone) || !message) {
    return res.render("contact", {
      pageTitle: "Contact",
      success: null,
      error: "Please fill all required fields.",
    });
  }

  const contacts = readJson(CONTACTS_FILE);
  contacts.push({
    id: "C" + Date.now(),
    name,
    email: email || null,
    phone: phone || null,
    message,
    status: "Pending",
    createdAt: new Date().toISOString(),
  });
  writeJson(CONTACTS_FILE, contacts);

  res.render("contact", {
    pageTitle: "Contact",
    success: "Thank you! We will contact you soon.",
    error: null,
  });
});

app.get("/about", (req, res) => {
  res.render("about", { pageTitle: "About" });
});

// === Start server ===
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Navya Jewels server running on http://localhost:${PORT}`);
});
