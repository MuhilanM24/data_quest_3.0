import "./globals.css";
export const metadata = { title: "PRISM Engine", description: "A clearer way to choose what is next." };
export default function RootLayout({ children }: { children: React.ReactNode }) { return <html lang="en"><body>{children}</body></html>; }
