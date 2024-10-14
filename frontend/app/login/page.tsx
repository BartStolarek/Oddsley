'use client'

import React, { useState } from 'react'
import { Input } from "@nextui-org/input"
import { Button } from "@nextui-org/button"
import { Card, CardBody, CardHeader, CardFooter } from "@nextui-org/card"
import { Link } from "@nextui-org/link"
import { title, subtitle } from "@/components/primitives"

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Add your authentication logic here
    console.log(isLogin ? 'Login submitted' : 'Signup submitted')
  }

  const toggleAuthMode = () => {
    setIsLogin(!isLogin)
  }

  return (
    <section className="flex flex-col items-center justify-start min-h-screen py-8 md:py-10 gap-8">
      <div className="text-center">
        <span className={title()}>Access your&nbsp;</span>
        <span className={title({ color: "violet" })}>account&nbsp;</span>
      </div>
      <Card className="w-full max-w-md">
        <CardHeader className="flex flex-col items-center pb-0 w-full">
          <h2 className={subtitle({ class: "text-center" })}>{isLogin ? 'Login' : 'Sign Up'}</h2>
        </CardHeader>
        <CardBody>
          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <Input
                type="text"
                label="Username"
                placeholder="Enter your username"
                required
              />
            )}
            <Input
              type="email"
              label="Email"
              placeholder="Enter your email"
              required
            />
            <Input
              type="password"
              label="Password"
              placeholder="Enter your password"
              required
            />
            {!isLogin && (
              <Input
                type="password"
                label="Confirm Password"
                placeholder="Confirm your password"
                required
              />
            )}
            <Button 
              color="primary" 
              type="submit" 
              fullWidth
            >
              {isLogin ? 'Sign In' : 'Sign Up'}
            </Button>
          </form>
        </CardBody>
        <CardFooter className="flex justify-center">
          <p>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <Link
              href="#"
              onClick={(e) => {
                e.preventDefault()
                toggleAuthMode()
              }}
            >
              {isLogin ? 'Sign up' : 'Login'}
            </Link>
          </p>
        </CardFooter>
      </Card>
    </section>
  )
}