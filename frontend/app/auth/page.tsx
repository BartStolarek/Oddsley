"use client";

import React, { useState } from "react";
import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/button";
import { Card, CardBody, CardHeader, CardFooter } from "@nextui-org/card";
import { Link } from "@nextui-org/link";

import { title, subtitle } from "@/components/primitives";
import { login, register } from "@/api/auth";
import { useRouter } from "next/navigation";

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    first_name: "",
    last_name: "",
  });
  const [error, setError] = useState("");
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      if (isLogin) {
        const data = await login({
          username: formData.username,
          password: formData.password,
        });
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        router.push("/");
      } else {
        if (formData.password !== formData.confirmPassword) {
          setError("Passwords do not match");
          return;
        }
        await register({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          first_name: formData.first_name,
          last_name: formData.last_name,
        });
        setIsLogin(true);
        setError("Registration successful. Please log in.");
      }
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("An unexpected error occurred");
      }
    }
  };

  const toggleAuthMode = () => {
    setIsLogin(!isLogin);
    setError("");
  };

  return (
    <section className="flex flex-col items-center justify-start min-h-screen py-8 md:py-10 gap-8">
      <div className="text-center">
        <span className={title()}>Access your&nbsp;</span>
        <span className={title({ color: "violet" })}>account&nbsp;</span>
      </div>
      <Card className="w-full max-w-md">
        <CardHeader className="flex flex-col items-center pb-0 w-full">
          <h2 className={subtitle({ class: "text-center" })}>
            {isLogin ? "Login" : "Sign Up"}
          </h2>
        </CardHeader>
        <CardBody>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <Input
              label="Username"
              name="username"
              onChange={handleChange}
              placeholder="Enter your username"
              required
              type="text"
              value={formData.username}
            />
            {!isLogin && (
              <Input
                label="Email"
                name="email"
                onChange={handleChange}
                placeholder="Enter your email"
                required
                type="email"
                value={formData.email}
              />
            )}
            <Input
              label="Password"
              name="password"
              onChange={handleChange}
              placeholder="Enter your password"
              required
              type="password"
              value={formData.password}
            />
            {!isLogin && (
              <Input
                label="Confirm Password"
                name="confirmPassword"
                onChange={handleChange}
                placeholder="Confirm your password"
                required
                type="password"
                value={formData.confirmPassword}
              />
            )}
            {error && <p className="text-red-500">{error}</p>}
            <Button color="primary" fullWidth type="submit">
              {isLogin ? "Sign In" : "Sign Up"}
            </Button>
          </form>
        </CardBody>
        <CardFooter className="flex justify-center">
          <p>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <Link href="#" onClick={toggleAuthMode}>
              {isLogin ? "Sign up" : "Login"}
            </Link>
          </p>
        </CardFooter>
      </Card>
    </section>
  );
}