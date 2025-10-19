// Configuración
const API_URL = 'http://localhost:5000/api';

// Estado global
let userToken = localStorage.getItem('userToken') || null;
let currentUser = JSON.parse(localStorage.getItem('currentUser')) || null;
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let favorites = [];
let allProducts = [];
let isLoginMode = true;

// ==================== INICIALIZACIÓN ====================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadProducts();
    
    if (userToken) {
        loadFavorites();
    }
});

function initializeApp() {
    updateUIBasedOnAuth();
    updateCartCount();
}

function setupEventListeners() {
    // Navegación
    document.getElementById('loginBtn').addEventListener('click', handleLoginClick);
    document.getElementById('cartBtn').addEventListener('click', () => openCartModal());
    document.getElementById('searchBtn').addEventListener('click', () => openSearchModal());
    document.getElementById('profileBtn')?.addEventListener('click', () => openProfileModal());
    document.getElementById('favoritesBtn')?.addEventListener('click', () => openFavoritesModal());
    document.getElementById('adminBtn')?.addEventListener('click', () => openAdminModal());
    
    // Cerrar modales
    document.querySelectorAll('.close').forEach(btn => {
        btn.addEventListener('click', closeAllModals);
    });
    
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            closeAllModals();
        }
    });
    
    // Auth
    document.getElementById('authForm').addEventListener('submit', handleAuthSubmit);
    document.getElementById('switchAuthMode').querySelector('a').addEventListener('click', toggleAuthMode);
    
    // Búsqueda
    document.getElementById('searchButton').addEventListener('click', performSearch);
    document.getElementById('searchInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });
    
    // Filtros
    document.getElementById('applyFilters').addEventListener('click', applyFilters);
    
    // Pago
    document.getElementById('paymentForm')?.addEventListener('submit', processPayment);
    document.getElementById('checkoutBtn').addEventListener('click', initiateCheckout);
    
    // Newsletter
    document.getElementById('contactForm').addEventListener('submit', handleNewsletter);
    
    // Formato de tarjeta
    const cardNumber = document.getElementById('cardNumber');
    cardNumber?.addEventListener('input', formatCardNumber);
    
    const cardExpiry = document.getElementById('cardExpiry');
    cardExpiry?.addEventListener('input', formatCardExpiry);
}

// ==================== AUTENTICACIÓN ====================

function handleLoginClick(e) {
    e.preventDefault();
    if (userToken) {
        logout();
    } else {
        openLoginModal();
    }
}

async function handleAuthSubmit(e) {
    e.preventDefault();
    if (isLoginMode) {
        await handleLogin();
    } else {
        await handleRegister();
    }
}

async function handleLogin() {
    const email = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            userToken = data.token;
            currentUser = data.usuario;
            localStorage.setItem('userToken', userToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            
            showNotification(`¡Bienvenido/a ${currentUser.nombre}!`, 'success');
            closeAllModals();
            updateUIBasedOnAuth();
            loadFavorites();
        } else {
            showNotification(data.mensaje || 'Error al iniciar sesión', 'error');
        }
    } catch (error) {
        showNotification('Error de conexión', 'error');
    }
}

async function handleRegister() {
    const nombre = document.getElementById('registerName').value;
    const email = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_URL}/registro`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ nombre, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success');
            toggleAuthMode();
            document.getElementById('authForm').reset();
        } else {
            showNotification(data.mensaje || 'Error al registrarse', 'error');
        }
    } catch (error) {
        showNotification('Error de conexión', 'error');
    }
}

function logout() {
    userToken = null;
    currentUser = null;
    favorites = [];
    localStorage.removeItem('userToken');
    localStorage.removeItem('currentUser');
    showNotification('Sesión cerrada exitosamente', 'success');
    updateUIBasedOnAuth();
}

function updateUIBasedOnAuth() {
    const loginBtn = document.getElementById('loginBtn');
    const profileBtn = document.getElementById('profileBtn');
    const favoritesBtn = document.getElementById('favoritesBtn');
    const adminBtn = document.getElementById('adminBtn');
    
    if (userToken && currentUser) {
        loginBtn.textContent = `${currentUser.nombre} | Salir`;
        profileBtn.style.display = 'inline-block';
        favoritesBtn.style.display = 'inline-block';
        
        if (currentUser.es_admin) {
            adminBtn.style.display = 'inline-block';
        }
    } else {
        loginBtn.textContent = 'Login';
        profileBtn.style.display = 'none';
        favoritesBtn.style.display = 'none';
        adminBtn.style.display = 'none';
    }
}

function toggleAuthMode(e) {
    if (e) e.preventDefault();
    isLoginMode = !isLoginMode;
    
    const modalTitle = document.getElementById('modalTitle');
    const authSubmitBtn = document.getElementById('authSubmitBtn');
    const switchAuthMode = document.getElementById('switchAuthMode');
    const nameGroup = document.getElementById('nameGroup');
    
    if (isLoginMode) {
        modalTitle.textContent = 'INICIAR SESIÓN';
        authSubmitBtn.textContent = 'Ingresar';
        switchAuthMode.innerHTML = '¿No tienes una cuenta? <a href="#">Regístrate aquí</a>';
        nameGroup.style.display = 'none';
    } else {
        modalTitle.textContent = 'REGISTRARSE';
        authSubmitBtn.textContent = 'Registrarse';
        switchAuthMode.innerHTML = '¿Ya tienes cuenta? <a href="#">Inicia sesión aquí</a>';
        nameGroup.style.display = 'block';
    }
    
    document.getElementById('authForm').reset();
    switchAuthMode.querySelector('a').addEventListener('click', toggleAuthMode);
}

// ==================== PRODUCTOS ====================

async function loadProducts(filters = {}) {
    try {
        let url = `${API_URL}/productos?`;
        if (filters.categoria) url += `categoria=${filters.categoria}&`;
        if (filters.color) url += `color=${filters.color}&`;
        if (filters.orden) url += `orden=${filters.orden}&`;
        
        const response = await fetch(url);
        allProducts = await response.json();
        renderProducts(allProducts);
    } catch (error) {
        console.error('Error cargando productos:', error);
    }
}

function renderProducts(products) {
    const grid = document.getElementById('productsGrid');
    grid.innerHTML = '';
    
    products.forEach(product => {
        const isFavorite = favorites.some(f => f.producto_id === product.id);
        const card = createProductCard(product, isFavorite);
        grid.appendChild(card);
    });
}

function createProductCard(product, isFavorite = false) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
        <div class="product-favorite">
            <button class="favorite-btn ${isFavorite ? 'active' : ''}" onclick="toggleFavorite(${product.id})">
                <i class="fas fa-heart"></i>
            </button>
        </div>
        <img src="${product.imagen_url}" alt="${product.nombre}">
        <h3 class="product-name">${product.nombre}</h3>
        <p class="product-description">${product.descripcion}</p>
        <p class="product-stock">Stock: ${product.stock}</p>
        <button class="product-price" onclick="addToCartDirect(${product.id}, '${product.nombre}', ${product.precio}, '${product.imagen_url}')">
            ${product.precio.toLocaleString()} COP
        </button>
    `;
    return card;
}

function applyFilters() {
    const filters = {
        categoria: document.getElementById('filterCategory').value,
        color: document.getElementById('filterColor').value,
        orden: document.getElementById('filterPrice').value
    };
    loadProducts(filters);
}

async function performSearch() {
    const searchInput = document.getElementById('searchInput').value.trim();
    const searchResults = document.getElementById('searchResults');
    
    if (!searchInput) {
        showNotification('Ingresa un término de búsqueda', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/productos/buscar?q=${encodeURIComponent(searchInput)}`);
        const products = await response.json();
        
        if (products.length === 0) {
            searchResults.innerHTML = '<p class="no-results">No se encontraron productos</p>';
            return;
        }
        
        let html = '<div class="search-results-grid">';
        products.forEach(product => {
            html += `
                <div class="product-card">
                    <img src="${product.imagen_url}" alt="${product.nombre}">
                    <h3 class="product-name">${product.nombre}</h3>
                    <button class="product-price" onclick="addToCartDirect(${product.id}, '${product.nombre}', ${product.precio}, '${product.imagen_url}')">
                        ${product.precio.toLocaleString()} COP
                    </button>
                </div>
            `;
        });
        html += '</div>';
        searchResults.innerHTML = html;
    } catch (error) {
        showNotification('Error al buscar', 'error');
    }
}

// ==================== CARRITO ====================

function addToCartDirect(id, name, price, image) {
    const product = { id, name, price, image, quantity: 1 };
    const existingProduct = cart.find(item => item.id === id);
    
    if (existingProduct) {
        existingProduct.quantity += 1;
        showNotification('Cantidad actualizada', 'success');
    } else {
        cart.push(product);
        showNotification(`"${name}" añadido al carrito! 🛍️`, 'success');
    }
    
    saveCart();
    updateCartCount();
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function updateCartCount() {
    const cartCount = document.getElementById('cartCount');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
}

function renderCart() {
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">Tu carrito está vacío</p>';
        cartTotal.textContent = '$0 COP';
        return;
    }
    
    let total = 0;
    let html = '';
    
    cart.forEach(item => {
        const subtotal = item.price * item.quantity;
        total += subtotal;
        
        html += `
            <div class="cart-item">
                <img src="${item.image}" alt="${item.name}">
                <div class="cart-item-details">
                    <h4>${item.name}</h4>
                    <p>$${item.price.toLocaleString()} COP</p>
                </div>
                <div class="cart-item-quantity">
                    <button onclick="updateCartQuantity('${item.id}', ${item.quantity - 1})">-</button>
                    <span>${item.quantity}</span>
                    <button onclick="updateCartQuantity('${item.id}', ${item.quantity + 1})">+</button>
                </div>
                <div class="cart-item-subtotal">
                    <p>$${subtotal.toLocaleString()} COP</p>
                    <button onclick="removeFromCart('${item.id}')" class="remove-btn">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    });
    
    cartItems.innerHTML = html;
    cartTotal.textContent = `${total.toLocaleString()} COP`;
}

function updateCartQuantity(productId, quantity) {
    const product = cart.find(item => item.id === productId);
    if (product) {
        if (quantity <= 0) {
            removeFromCart(productId);
        } else {
            product.quantity = quantity;
            saveCart();
            renderCart();
        }
    }
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveCart();
    updateCartCount();
    renderCart();
    showNotification('Producto eliminado del carrito', 'success');
}

// ==================== FAVORITOS ====================

async function loadFavorites() {
    if (!userToken) return;
    
    try {
        const response = await fetch(`${API_URL}/favoritos`, {
            headers: { 'Authorization': `Bearer ${userToken}` }
        });
        favorites = await response.json();
        updateFavoritesCount();
    } catch (error) {
        console.error('Error cargando favoritos:', error);
    }
}

async function toggleFavorite(productId) {
    if (!userToken) {
        showNotification('Debes iniciar sesión', 'error');
        openLoginModal();
        return;
    }
    
    const isFavorite = favorites.some(f => f.producto_id === productId);
    
    try {
        if (isFavorite) {
            const response = await fetch(`${API_URL}/favoritos/${productId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${userToken}` }
            });
            if (response.ok) {
                showNotification('Eliminado de favoritos', 'success');
                loadFavorites();
                loadProducts();
            }
        } else {
            const response = await fetch(`${API_URL}/favoritos`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${userToken}`
                },
                body: JSON.stringify({ producto_id: productId })
            });
            if (response.ok) {
                showNotification('Agregado a favoritos ❤️', 'success');
                loadFavorites();
                loadProducts();
            }
        }
    } catch (error) {
        showNotification('Error al actualizar favoritos', 'error');
    }
}

function updateFavoritesCount() {
    const favCount = document.getElementById('favCount');
    favCount.textContent = favorites.length;
}

function renderFavorites() {
    const favoritesItems = document.getElementById('favoritesItems');
    
    if (favorites.length === 0) {
        favoritesItems.innerHTML = '<p class="empty-cart">No tienes favoritos aún</p>';
        return;
    }
    
    let html = '';
    favorites.forEach(fav => {
        html += `
            <div class="cart-item">
                <img src="${fav.producto.imagen_url}" alt="${fav.producto.nombre}">
                <div class="cart-item-details">
                    <h4>${fav.producto.nombre}</h4>
                    <p>${fav.producto.precio.toLocaleString()} COP</p>
                </div>
                <div class="favorite-actions">
                    <button onclick="addToCartDirect(${fav.producto.id}, '${fav.producto.nombre}', ${fav.producto.precio}, '${fav.producto.imagen_url}')" class="add-to-cart-btn">
                        <i class="fas fa-shopping-cart"></i> Añadir al Carrito
                    </button>
                    <button onclick="toggleFavorite(${fav.producto.id})" class="remove-btn">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    });
    
    favoritesItems.innerHTML = html;
}

// ==================== PERFIL ====================

async function loadProfile() {
    try {
        const response = await fetch(`${API_URL}/perfil`, {
            headers: { 'Authorization': `Bearer ${userToken}` }
        });
        const profile = await response.json();
        renderProfileInfo(profile);
    } catch (error) {
        showNotification('Error al cargar perfil', 'error');
    }
}

function renderProfileInfo(profile) {
    const content = document.getElementById('profileContent');
    content.innerHTML = `
        <form id="profileForm" class="profile-form">
            <div class="form-group">
                <label>Nombre</label>
                <input type="text" id="profileName" value="${profile.nombre || ''}" required>
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" value="${profile.email}" disabled>
            </div>
            <div class="form-group">
                <label>Teléfono</label>
                <input type="tel" id="profilePhone" value="${profile.telefono || ''}">
            </div>
            <div class="form-group">
                <label>Dirección</label>
                <textarea id="profileAddress">${profile.direccion || ''}</textarea>
            </div>
            <div class="form-group">
                <label>Ciudad</label>
                <input type="text" id="profileCity" value="${profile.ciudad || ''}">
            </div>
            <button type="submit" class="login-btn">Actualizar Perfil</button>
        </form>
        <p class="profile-date">Miembro desde: ${profile.fecha_registro}</p>
    `;
    
    document.getElementById('profileForm').addEventListener('submit', updateProfile);
}

async function updateProfile(e) {
    e.preventDefault();
    
    const data = {
        nombre: document.getElementById('profileName').value,
        telefono: document.getElementById('profilePhone').value,
        direccion: document.getElementById('profileAddress').value,
        ciudad: document.getElementById('profileCity').value
    };
    
    try {
        const response = await fetch(`${API_URL}/perfil`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken}`
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            currentUser.nombre = data.nombre;
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            showNotification('Perfil actualizado exitosamente', 'success');
            updateUIBasedOnAuth();
        }
    } catch (error) {
        showNotification('Error al actualizar perfil', 'error');
    }
}

async function loadOrders() {
    try {
        const response = await fetch(`${API_URL}/pedidos`, {
            headers: { 'Authorization': `Bearer ${userToken}` }
        });
        const orders = await response.json();
        renderOrders(orders);
    } catch (error) {
        showNotification('Error al cargar pedidos', 'error');
    }
}

function renderOrders(orders) {
    const content = document.getElementById('profileContent');
    
    if (orders.length === 0) {
        content.innerHTML = '<p class="empty-cart">No tienes pedidos aún</p>';
        return;
    }
    
    let html = '<div class="orders-list">';
    orders.forEach(order => {
        html += `
            <div class="order-card">
                <div class="order-header">
                    <h3>Pedido #${order.numero_pedido}</h3>
                    <span class="order-status status-${order.estado.toLowerCase()}">${order.estado}</span>
                </div>
                <p class="order-date">Fecha: ${order.fecha_pedido}</p>
                <p class="order-total">Total: ${order.total.toLocaleString()} COP</p>
                <div class="order-items">
                    ${order.items.map(item => `
                        <div class="order-item">
                            <img src="${item.producto.imagen_url}" alt="${item.producto.nombre}">
                            <span>${item.producto.nombre} x${item.cantidad}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    });
    html += '</div>';
    
    content.innerHTML = html;
}

// ==================== PAGO ====================

function initiateCheckout() {
    if (cart.length === 0) {
        showNotification('Tu carrito está vacío', 'error');
        return;
    }
    
    if (!userToken) {
        showNotification('Debes iniciar sesión', 'error');
        closeAllModals();
        openLoginModal();
        return;
    }
    
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    document.getElementById('paymentTotal').textContent = `${total.toLocaleString()} COP`;
    
    closeAllModals();
    openPaymentModal();
}

async function processPayment(e) {
    e.preventDefault();
    
    const cardNumber = document.getElementById('cardNumber').value.replace(/\s/g, '');
    const cardName = document.getElementById('cardName').value;
    const shippingAddress = document.getElementById('shippingAddress').value;
    
    // Validar tarjetas de prueba
    let paymentSuccess = false;
    if (cardNumber === '4242424242424242') {
        paymentSuccess = true;
    } else if (cardNumber === '4000000000000002') {
        paymentSuccess = false;
    } else {
        showNotification('Usa una tarjeta de prueba válida', 'error');
        return;
    }
    
    if (!paymentSuccess) {
        showNotification('Pago rechazado. Intenta con otra tarjeta.', 'error');
        return;
    }
    
    // Sincronizar carrito con backend antes de crear pedido
    try {
        // Primero sincronizar cada item del carrito local con el backend
        for (const item of cart) {
            await fetch(`${API_URL}/carrito`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${userToken}`
                },
                body: JSON.stringify({
                    producto_id: item.id,
                    cantidad: item.quantity
                })
            });
        }
        
        // Crear pedido
        const response = await fetch(`${API_URL}/pedidos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken}`
            },
            body: JSON.stringify({
                metodo_pago: 'Tarjeta de Crédito',
                direccion_envio: shippingAddress
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            cart = [];
            saveCart();
            updateCartCount();
            
            showNotification(`¡Pago exitoso! 🎉 Pedido #${data.numero_pedido}`, 'success');
            closeAllModals();
            
            // Mostrar resumen
            setTimeout(() => {
                alert(`✅ PEDIDO CONFIRMADO\n\nNúmero de Pedido: ${data.numero_pedido}\nTotal: ${data.total.toLocaleString()} COP\n\nGracias por tu compra en GLAM RENT!`);
            }, 500);
        } else {
            showNotification(data.mensaje || 'Error al crear el pedido', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al procesar el pago', 'error');
    }
}

function formatCardNumber(e) {
    let value = e.target.value.replace(/\s/g, '');
    let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
    e.target.value = formattedValue;
}

function formatCardExpiry(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
    }
    e.target.value = value;
}

// ==================== ADMIN ====================

async function loadAdminPanel() {
    renderAdminTabs();
    await loadAdminOrders();
}

function renderAdminTabs() {
    const content = document.getElementById('adminContent');
    content.innerHTML = `
        <div class="admin-tabs">
            <button class="admin-tab-btn active" onclick="loadAdminOrders()">Pedidos</button>
            <button class="admin-tab-btn" onclick="loadAdminProducts()">Productos</button>
        </div>
        <div id="adminTabContent" class="admin-tab-content"></div>
    `;
}

async function loadAdminOrders() {
    try {
        // Activar tab
        document.querySelectorAll('.admin-tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.admin-tab-btn')[0].classList.add('active');
        
        const response = await fetch(`${API_URL}/admin/pedidos`, {
            headers: { 'Authorization': `Bearer ${userToken}` }
        });
        const orders = await response.json();
        renderAdminOrders(orders);
    } catch (error) {
        showNotification('Error al cargar pedidos', 'error');
    }
}

async function loadAdminProducts() {
    try {
        // Activar tab
        document.querySelectorAll('.admin-tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.admin-tab-btn')[1].classList.add('active');
        
        const response = await fetch(`${API_URL}/admin/productos`, {
            headers: { 'Authorization': `Bearer ${userToken}` }
        });
        const products = await response.json();
        renderAdminProducts(products);
    } catch (error) {
        showNotification('Error al cargar productos', 'error');
    }
}

function renderAdminOrders(orders) {
    const content = document.getElementById('adminTabContent');
    
    if (orders.length === 0) {
        content.innerHTML = '<p class="empty-cart">No hay pedidos</p>';
        return;
    }
    
    let html = `
        <div class="admin-stats">
            <div class="stat-card">
                <h3>${orders.length}</h3>
                <p>Total Pedidos</p>
            </div>
            <div class="stat-card">
                <h3>${orders.reduce((sum, o) => sum + o.total, 0).toLocaleString()}</h3>
                <p>Ingresos Totales</p>
            </div>
            <div class="stat-card">
                <h3>${orders.filter(o => o.estado === 'Pendiente').length}</h3>
                <p>Pedidos Pendientes</p>
            </div>
        </div>
        <div class="orders-list">
    `;
    
    orders.forEach(order => {
        html += `
            <div class="admin-order-card">
                <div class="order-header">
                    <div>
                        <h3>Pedido #${order.numero_pedido}</h3>
                        <p>Cliente: ${order.cliente.nombre} (${order.cliente.email})</p>
                        <p>Fecha: ${order.fecha_pedido}</p>
                        <p>Dirección: ${order.direccion_envio || 'No especificada'}</p>
                    </div>
                    <div>
                        <p class="order-total">${order.total.toLocaleString()} COP</p>
                        <select class="status-select" onchange="updateOrderStatus(${order.id}, this.value)">
                            <option value="Pendiente" ${order.estado === 'Pendiente' ? 'selected' : ''}>Pendiente</option>
                            <option value="Procesando" ${order.estado === 'Procesando' ? 'selected' : ''}>Procesando</option>
                            <option value="Enviado" ${order.estado === 'Enviado' ? 'selected' : ''}>Enviado</option>
                            <option value="Entregado" ${order.estado === 'Entregado' ? 'selected' : ''}>Entregado</option>
                            <option value="Cancelado" ${order.estado === 'Cancelado' ? 'selected' : ''}>Cancelado</option>
                        </select>
                    </div>
                </div>
                <div class="order-items">
                    ${order.items.map(item => `
                        <div class="order-item">
                            <img src="${item.producto.imagen_url}" alt="${item.producto.nombre}">
                            <span>${item.producto.nombre} x${item.cantidad} - ${item.precio_unitario.toLocaleString()}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    content.innerHTML = html;
}

function renderAdminProducts(products) {
    const content = document.getElementById('adminTabContent');
    
    let html = `
        <div class="admin-products-header">
            <h3>Gestión de Productos</h3>
            <button class="login-btn" onclick="showAddProductForm()">Agregar Producto</button>
        </div>
        <div class="admin-products-grid">
    `;
    
    products.forEach(product => {
        html += `
            <div class="admin-product-card">
                <img src="${product.imagen_url}" alt="${product.nombre}" onerror="this.src='imagenes/logo.png'">
                <div class="admin-product-info">
                    <h4>${product.nombre}</h4>
                    <p class="product-price">${product.precio.toLocaleString()} COP</p>
                    <p class="product-category">${product.categoria} - ${product.color}</p>
                    <div class="stock-control">
                        <label>Stock:</label>
                        <input type="number" value="${product.stock}" min="0" 
                               onchange="updateProductStock(${product.id}, this.value)" 
                               class="stock-input">
                    </div>
                    <div class="admin-product-actions">
                        <button onclick="editProduct(${product.id})" class="edit-btn">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button onclick="deleteProduct(${product.id})" class="delete-btn">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    content.innerHTML = html;
}

async function updateOrderStatus(orderId, newStatus) {
    try {
        const response = await fetch(`${API_URL}/admin/pedidos/${orderId}/estado`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken}`
            },
            body: JSON.stringify({ estado: newStatus })
        });
        
        if (response.ok) {
            showNotification('Estado actualizado', 'success');
            loadAdminOrders();
        }
    } catch (error) {
        showNotification('Error al actualizar estado', 'error');
    }
}

async function updateProductStock(productId, newStock) {
    try {
        const response = await fetch(`${API_URL}/admin/productos/${productId}/stock`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken}`
            },
            body: JSON.stringify({ stock: parseInt(newStock) })
        });
        
        if (response.ok) {
            showNotification('Stock actualizado', 'success');
            // Recargar productos en la vista principal
            loadProducts();
        } else {
            const data = await response.json();
            showNotification(data.mensaje || 'Error al actualizar stock', 'error');
        }
    } catch (error) {
        showNotification('Error al actualizar stock', 'error');
    }
}

function showAddProductForm() {
    const content = document.getElementById('adminTabContent');
    content.innerHTML = `
        <div class="admin-form-container">
            <h3>Agregar Nuevo Producto</h3>
            <form id="addProductForm" class="admin-product-form">
                <div class="form-row">
                    <div class="form-group">
                        <label>Nombre</label>
                        <input type="text" id="productName" required>
                    </div>
                    <div class="form-group">
                        <label>Precio (COP)</label>
                        <input type="number" id="productPrice" min="0" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Categoría</label>
                        <select id="productCategory" required>
                            <option value="vestido">Vestido</option>
                            <option value="corset">Corsé</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Color</label>
                        <input type="text" id="productColor">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Talla</label>
                        <input type="text" id="productSize">
                    </div>
                    <div class="form-group">
                        <label>Stock</label>
                        <input type="number" id="productStock" min="0" value="0">
                    </div>
                </div>
                <div class="form-group">
                    <label>Descripción</label>
                    <textarea id="productDescription"></textarea>
                </div>
                <div class="form-group">
                    <label>URL de Imagen</label>
                    <input type="url" id="productImage">
                </div>
                <div class="form-actions">
                    <button type="submit" class="login-btn">Crear Producto</button>
                    <button type="button" onclick="loadAdminProducts()" class="cancel-btn">Cancelar</button>
                </div>
            </form>
        </div>
    `;
    
    document.getElementById('addProductForm').addEventListener('submit', createProduct);
}

async function createProduct(e) {
    e.preventDefault();
    
    const productData = {
        nombre: document.getElementById('productName').value,
        precio: parseFloat(document.getElementById('productPrice').value),
        categoria: document.getElementById('productCategory').value,
        color: document.getElementById('productColor').value,
        talla: document.getElementById('productSize').value,
        stock: parseInt(document.getElementById('productStock').value),
        descripcion: document.getElementById('productDescription').value,
        imagen_url: document.getElementById('productImage').value
    };
    
    try {
        const response = await fetch(`${API_URL}/admin/productos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken}`
            },
            body: JSON.stringify(productData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('Producto creado exitosamente', 'success');
            loadAdminProducts();
            loadProducts(); // Recargar productos en la vista principal
        } else {
            showNotification(data.mensaje || 'Error al crear producto', 'error');
        }
    } catch (error) {
        showNotification('Error al crear producto', 'error');
    }
}

async function deleteProduct(productId) {
    if (!confirm('¿Estás seguro de que quieres eliminar este producto?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/admin/productos/${productId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${userToken}`
            }
        });
        
        if (response.ok) {
            showNotification('Producto eliminado', 'success');
            loadAdminProducts();
            loadProducts(); // Recargar productos en la vista principal
        } else {
            const data = await response.json();
            showNotification(data.mensaje || 'Error al eliminar producto', 'error');
        }
    } catch (error) {
        showNotification('Error al eliminar producto', 'error');
    }
}

function editProduct(productId) {
    // Esta función se puede implementar más tarde para editar productos existentes
    showNotification('Función de edición en desarrollo', 'info');
}

// ==================== MODALES ====================

function openLoginModal() {
    document.getElementById('loginModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function openCartModal() {
    renderCart();
    document.getElementById('cartModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function openSearchModal() {
    document.getElementById('searchModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function openFavoritesModal() {
    renderFavorites();
    document.getElementById('favoritesModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function openProfileModal() {
    document.getElementById('profileModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            if (this.dataset.tab === 'info') {
                loadProfile();
            } else if (this.dataset.tab === 'orders') {
                loadOrders();
            }
        });
    });
    
    loadProfile();
}

function openPaymentModal() {
    document.getElementById('paymentModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function openAdminModal() {
    document.getElementById('adminModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    loadAdminPanel();
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
    document.body.style.overflow = 'auto';
}

// ==================== NEWSLETTER ====================

function handleNewsletter(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const name = document.getElementById('name').value;
    
    showNotification('¡Gracias por suscribirte! 📧', 'success');
    document.getElementById('contactForm').reset();
}

// ==================== UTILIDADES ====================

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#F0C5CE' : '#ff4757'};
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    document.body.appendChild(notification);
    setTimeout(() => notification.style.transform = 'translateX(0)', 100);
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => document.body.removeChild(notification), 300);
    }, 3000);
}