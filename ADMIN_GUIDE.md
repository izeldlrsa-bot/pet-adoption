# Admin Panel - Adoption Application Management Guide

## Overview
The admin panel allows administrators to view, manage, and make decisions on user adoption applications. This document explains how to access and use the application management features.

---

## 🔑 Accessing the Admin Panel

### For Admins:
1. **Navigate to the Admin Dashboard**: 
   - Login as an admin user
   - Click on the **Admin** dropdown in the navbar
   - Select **Admin Dashboard**
   - Or go to: `http://127.0.0.1:8000/adoption/admin/`

2. **Access Applications**:
   - From Admin Dashboard, click **"Review Applications"** button
   - Or go directly to: `http://127.0.0.1:8000/adoption/applications/`

---

## 📊 Admin Dashboard Features

The Admin Dashboard provides an overview of the system with quick stats:

### Quick Stats Cards:
- **Total Pets**: Total number of pets in the system
- **Available Pets**: Pets that are available for adoption
- **Adopted Pets**: Pets that have been adopted
- **Pending Applications**: Applications waiting to be reviewed

### Quick Action Cards:
- **Review Applications**: Navigate to view all adoption applications
- **Add New Pet**: Add a new adoptable pet to the system
- **Manage Pets**: View and edit existing pets

### Recent Applications:
- Shows the 5 most recent applications
- Displays applicant info, pet name, applied date, and status
- Quick access to review each application

---

## 📋 Managing Applications

### Viewing All Applications

Access the Applications List page (`/adoption/applications/`):

1. **View Overview Stats**:
   - Total applications
   - Count by status (Pending, Under Review, Approved, Rejected, Cancelled)

2. **Filter Applications**:
   - **By Status**: Select a status filter (All, Pending, Under Review, Approved, Rejected, Cancelled)
   - **By Search**: Search by applicant name, pet name, email, or phone

3. **Application Table**:
   - Shows all filtered applications in a table
   - Columns: ID, Applicant, Pet, Applied Date, Status, Actions
   - Each row has a "Review" button to view details

---

## ✅ Reviewing Applications

### Application Review Page

Click "Review" on any application to view full details and make a decision.

#### What You'll See:

**Left Side:**
- **Applicant Information**:
  - Name, email, phone, address
  - Applied date and review/decision timestamps
  
- **Pet Information**:
  - Pet name, breed, age
  - Current adoption status

**Right Side - Review Form:**
- **Application Responses** (read-only):
  - Why they want to adopt
  - Previous pet experience
  - Home environment description
  - Household members info
  - Veterinary and personal references

- **Admin Decision Section**:
  - **Status Dropdown**: Select application status
    - Pending (default)
    - Under Review
    - Approved ✅
    - Rejected ❌
    - Cancelled
  
  - **Admin Notes**: Private notes visible only to admins
  - **Internal Comments**: Additional internal notes
  - **Follow-up Date**: Schedule a follow-up if needed
  - **Follow-up Notes**: Notes for follow-up contact

#### Important: What Happens When You Approve/Reject

- **When Status is Changed**: The system automatically sets the reviewed date and decision date
- **When Application is Approved**: 
  - The associated pet is marked as "adopted" and unavailable
  - Other pending/under-review applications for that pet may need to be rejected
- **When Application is Rejected**: 
  - The pet remains available for other applications

---

## 🚀 Application Workflow

### Typical Application Lifecycle:

1. **User Applies** (Status: `Pending`)
   - User submits adoption application form
   - Application appears in admin panel
   - Admin is notified of pending review

2. **Admin Reviews** (Status: `Under Review`)
   - Admin reads application details
   - Admin makes notes and comments
   - Admin can schedule follow-up date

3. **Admin Decides** (Status: `Approved` or `Rejected`)
   - **Approved**: Application is accepted
     - Pet is marked as adopted
     - User is notified (if email notification enabled)
   - **Rejected**: Application is declined
     - Pet remains available
     - User is notified (if email notification enabled)

4. **Follow-up** (Optional)
   - Admin can set follow-up date and notes
   - Used for post-adoption check-ins or denied applicants to offer other pets

---

## 📊 Application Status Guide

| Status | Meaning | Action |
|--------|---------|--------|
| **Pending** | New application, not yet reviewed | Review and make decision |
| **Under Review** | Being evaluated by admin | Continue review process |
| **Approved** | Application accepted | Pet marked as adopted |
| **Rejected** | Application declined | Pet remains available |
| **Cancelled** | Application cancelled by user or admin | No action needed |

---

## 🔔 Important Features

### For Admins:
✅ View all adoption applications  
✅ Search and filter applications  
✅ Review detailed applicant information  
✅ Make approval/rejection decisions  
✅ Add admin notes and internal comments  
✅ Schedule follow-ups  
✅ See application status history  

### Pet Management:
✅ When application is approved, pet is automatically marked as adopted  
✅ When approval is revoked, pet automatically becomes available again  
✅ One pet can have multiple applications, but only one approved at a time  

---

## 📌 Quick Tips

1. **Before Approving**: Always review all application responses carefully
2. **Add Notes**: Use admin notes to document your decision reasoning
3. **Follow-ups**: Set follow-up dates for post-adoption check-ins
4. **Search Feature**: Use search to quickly find applications by name, pet, or email
5. **Status Filters**: Filter by status to prioritize which applications to review first

---

## 🔒 Admin Permissions

- **Staff Users**: Can access application management features
- **Superusers**: Can also create admin accounts and access Django admin panel
- **Regular Users**: Can only view their own applications

---

## 📞 Support

If you need help with the admin panel:
1. Check the application model fields in `adoption/models.py`
2. Review form fields in `adoption/forms.py`
3. Check the admin configuration in `adoption/admin.py`

---

**Last Updated**: February 9, 2026  
**System**: Pet Adoption Management System  
**Django Version**: 6.0.2
