"use client";

import styled from "styled-components";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  return (
    <Nav>
      <NavItem isActive={pathname === "/"}>
        <Link href="/">Inicio</Link>
      </NavItem>
      <Separator>|</Separator>
      <NavItem isActive={pathname === "/dashboard"}>
        <Link href="/dashboard">Dashboard</Link>
      </NavItem>
    </Nav>
  );
}

const Nav = styled.nav`
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
`;

const NavItem = styled.div.attrs(({ isActive }) => ({}))`
  a {
    color: ${({ isActive }) => (isActive ? "#ffc66d" : "#a9b7c6")};
    text-decoration: none;
    font-size: 1.2rem;
    font-weight: bold;
    transition: color 0.3s, border-bottom 0.3s;

    &:hover {
      color: #cc7832;
    }

    border-bottom: ${({ isActive }) =>
      isActive ? "2px solid #ffc66d" : "none"};
    padding-bottom: 0.2rem;
  }
`;

const Separator = styled.span`
  color: #4e94ce;
  font-size: 1.2rem;
  font-weight: bold;
`;
