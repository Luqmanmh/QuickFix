import { useAuthStore } from '~/stores/auth';

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();

  if (!authStore.role) {
    return navigateTo("/login?message='not logged in'");
  }

  const allowedRoles = to.meta.role;
  const userRole = authStore.role ? authStore.role.toLowerCase() : "";

  if (allowedRoles && !allowedRoles.map((r) => r.toLowerCase()).includes(userRole)) {
    switch (userRole) {
      case 'admin':
        return router.push('/admin')
      case 'cashier':
        return navigateTo(`/cashier/scan`);
      case 'pharmacist':
        return navigateTo(`/pharmacist/manage`);
      default:
        return navigateTo(`/shop`);
    }
  }
});
