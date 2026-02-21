import * as React from "react"
import { Check, ChevronsUpDown, Search } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "@/components/ui/command"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"
import type { Country } from "@/types"

interface CountrySearchProps {
    countries: Country[]
    onSelect: (country: Country) => void
    selectedCountryId?: string
}

export function CountrySearch({ countries, onSelect, selectedCountryId }: CountrySearchProps) {
    const [open, setOpen] = React.useState(false)

    const selectedCountry = React.useMemo(() =>
        countries.find((c) => c.id === selectedCountryId),
        [countries, selectedCountryId]
    )

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button
                    variant="outline"
                    role="combobox"
                    aria-expanded={open}
                    className="w-[250px] justify-between bg-slate-900 border-slate-700 text-slate-300 hover:text-white hover:bg-slate-800"
                >
                    <div className="flex items-center gap-2">
                        <Search className="w-4 h-4 text-slate-500" />
                        <span className="truncate">
                            {selectedCountry ? selectedCountry.name : "Search country..."}
                        </span>
                    </div>
                    <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[250px] p-0 bg-slate-900 border-slate-700 shadow-2xl">
                <Command className="bg-slate-900 text-slate-300">
                    <CommandInput placeholder="Type country name..." className="h-9 border-none focus:ring-0 text-slate-200" />
                    <CommandEmpty className="py-2 px-4 text-sm text-slate-500">No country found.</CommandEmpty>
                    <CommandList className="max-h-[300px] overflow-y-auto">
                        <CommandGroup>
                            {countries.map((country) => (
                                <CommandItem
                                    key={country.id}
                                    // Use "ID name" so cmdk searches by name but each item is
                                    // globally unique — prevents cmdk from merging/collapsing
                                    // items that have similar names.
                                    value={`${country.id} ${country.name}`}
                                    onSelect={(val) => {
                                        // Extract the ID prefix from the compound value and
                                        // look the country up — guarantees correct selection
                                        // regardless of cmdk's internal normalisation.
                                        const id = val.split(' ')[0].toUpperCase();
                                        const found = countries.find((c) => c.id === id);
                                        if (found) {
                                            onSelect(found);
                                            setOpen(false);
                                        }
                                    }}
                                    className="flex items-center justify-between px-4 py-2 hover:bg-slate-800 cursor-pointer text-slate-300 hover:text-white"
                                >
                                    <div className="flex items-center gap-2">
                                        <span className="text-xs font-mono text-slate-500">{country.id}</span>
                                        <span>{country.name}</span>
                                    </div>
                                    <Check
                                        className={cn(
                                            "h-4 w-4 text-blue-500",
                                            selectedCountryId === country.id ? "opacity-100" : "opacity-0"
                                        )}
                                    />
                                </CommandItem>
                            ))}
                        </CommandGroup>
                    </CommandList>
                </Command>
            </PopoverContent>
        </Popover>
    )
}
