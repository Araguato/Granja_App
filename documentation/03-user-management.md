# User Management System

## 5.1 User Roles and Permissions

### 5.1.1 Role Definitions

#### Administrator (Administrador)
- **Full system access**
- User account management
- System configuration
- Access to all modules and functions
- Can override restrictions

#### Supervisor
- **Operational oversight**
- View all data across the system
- Approve/reject critical operations
- Generate and export reports
- Limited user management capabilities

#### Operator (Operador)
- **Daily operations**
- Data entry for assigned areas
- View only access to most modules
- Limited to own data and assigned galpones/lotes
- Cannot modify system settings

### 5.1.2 Permission Matrix

| Module/Feature | Administrator | Supervisor | Operator |
|----------------|---------------|------------|----------|
| **Dashboard** | View All | View All | View Assigned |
| **Granjas** | CRUD | CRUD | R |
| **Galpones** | CRUD | CRUD | R |
| **Lotes** | CRUD | CRUD | R |
| **Seguimiento** | CRUD | CRUD | CRU (Own) |
| **Alimentos** | CRUD | CRU | R |
| **Vacunas** | CRUD | CRU | R |
| **Ventas** | CRUD | CRU | - |
| **Clientes** | CRUD | CRU | - |
| **Reportes** | All Reports | All Reports | Limited |
| **Configuración** | Full Access | View | - |
| **Usuarios** | CRUD | R | - |

## 5.2 User Profile

### 5.2.1 UserProfile Model

#### Fields
| Field | Type | Description |
|-------|------|-------------|
| user | OneToOne → User | Django auth user |
| rol | String(20) | User role |
| telefono | String(20) | Contact number |
| direccion | Text | Physical address |
| fecha_nacimiento | Date | Date of birth |
| fecha_ingreso | Date | Employment start date |
| foto | Image | Profile picture |
| firma | Image | Digital signature |
| permisos_especiales | JSON | Additional permissions |
| estado | String(20) | Active/Inactive |
| fecha_creacion | DateTime | Account creation |

### 5.2.2 Authentication Flow

1. **Login Process**
   - Username/password authentication
   - JWT token generation
   - Session management
   - Failed login attempt tracking

2. **Password Management**
   - Secure password hashing
   - Password reset functionality
   - Password complexity requirements
   - Password expiration (90 days)

## 5.3 Access Control

### 5.3.1 Permission System

#### Built-in Permissions
- `avicola.view_dashboard`
- `produccion.add_lote`
- `produccion.change_lote`
- `produccion.delete_lote`
- `ventas.add_venta`
- `ventas.change_venta`
- `inventario.view_alimento`

#### Custom Permissions
- `can_approve_operations` (Supervisor+)
- `can_export_reports`
- `can_manage_users` (Admin only)
- `can_override_restrictions` (Admin only)

### 5.3.2 Row-Level Security
- Users can only see their own data unless they have elevated permissions
- Supervisors can see all data within their assigned region
- Administrators have unrestricted access

## 5.4 Security Features

### 5.4.1 Authentication
- JWT-based authentication
- Session timeout (30 minutes)
- Concurrent session control
- IP whitelisting (optional)

### 5.4.2 Authorization
- Role-based access control (RBAC)
- Attribute-based access control (ABAC)
- Permission caching for performance

### 5.4.3 Audit Logging
- User login/logout
- Sensitive operations
- Data modifications
- Permission changes

## 5.5 User Interface

### 5.5.1 User Management Console
- User listing with filters
- Role assignment
- Status toggling (active/inactive)
- Permission management

### 5.5.2 Profile Management
- Personal information
- Password change
- Two-factor authentication setup
- Session management

## 5.6 Integration

### 5.6.1 Active Directory/LDAP
- Optional integration with corporate directory
- Group synchronization
- Single Sign-On (SSO) support

### 5.6.2 API Access
- OAuth2 for API authentication
- API key management
- Rate limiting

## 5.7 Compliance

### 5.7.1 Data Protection
- Password encryption
- Sensitive data masking
- Audit trails

### 5.7.2 Regulatory Requirements
- GDPR compliance
- Data retention policies
- Right to be forgotten

## 5.8 User Lifecycle

### 5.8.1 Onboarding
1. Account creation by admin
2. Welcome email with temporary password
3. First login with password change
4. Initial training and orientation

### 5.8.2 Role Changes
1. Permission review
2. Approval workflow
3. Automatic access adjustment
4. Notification to user

### 5.8.3 Offboarding
1. Account deactivation
2. Data retention compliance
3. Access revocation
4. Final audit log

## 5.9 Emergency Procedures

### 5.9.1 Account Lockout
- Automatic after 5 failed attempts
- Manual lockout by admin
- Unlock procedure with verification

### 5.9.2 Security Incidents
- Suspicious activity detection
- Incident reporting
- Response protocol
- Post-incident review
