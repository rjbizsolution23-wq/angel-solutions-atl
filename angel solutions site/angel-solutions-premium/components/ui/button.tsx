import * as React from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-semibold ring-offset-background transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default:
          'bg-gradient-to-r from-brand-gold-500 to-brand-gold-600 text-white shadow-lg hover:shadow-xl hover:from-brand-gold-600 hover:to-brand-gold-700 luxury-button',
        primary:
          'bg-brand-purple-600 text-white shadow-lg hover:shadow-xl hover:bg-brand-purple-700',
        secondary:
          'bg-brand-navy-700 text-white shadow-lg hover:shadow-xl hover:bg-brand-navy-800',
        outline:
          'border-2 border-brand-gold-500 bg-transparent text-brand-gold-600 hover:bg-brand-gold-50 dark:text-brand-gold-400 dark:hover:bg-brand-gold-950/10',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-brand-gold-600 underline-offset-4 hover:underline dark:text-brand-gold-400',
        glass:
          'glass-card text-foreground hover:shadow-xl hover:scale-[1.02]',
      },
      size: {
        default: 'h-11 px-8 py-2.5',
        sm: 'h-9 px-4 text-xs',
        lg: 'h-14 px-10 text-base',
        xl: 'h-16 px-12 text-lg',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button'
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = 'Button'

export { Button, buttonVariants }
