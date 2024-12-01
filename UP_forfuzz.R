sharepoint_path <- Sys.getenv("REP2SI_DIR")

f_ind <- paste0(
  sharepoint_path,
  "/rep2si-data/up-data/restricted/UP_Indiv.csv"
)

f_par <- paste0(
  sharepoint_path,
  "/rep2si-data/up-data/de-identified/UP_Partnerships.csv"
)

indiv <- read.csv(f_ind, header = TRUE, as.is = TRUE)  %>% tibble

part <- read.csv(f_par, header = TRUE, as.is = TRUE)

deceased <- indiv$IndivID[which(indiv$is_living == 0)]

indiv <- data.frame(IndivID = indiv$IndivID, 
                  firstname = indiv$Name,
                  caste = indiv$Caste, 
                  age = indiv$Age,
                  gender = indiv$Gender, 
                  location = indiv$Location,
                  FatherID = indiv$FatherID,
                  MotherID = indiv$MotherID)

kin <- data.frame(IndivID = indiv$IndivID,
                  FatherID = indiv$FatherID,
                  MotherID = indiv$MotherID)


## parents not in partnerships
kin <- subset(kin, is.na(kin$FatherID) == FALSE)
missing <- kin[!paste(kin$Father, kin$Mother) %in% paste(part$Husband, part$Wife), c(2,3)]
missing <- missing[!duplicated(missing),]

if (nrow(missing) > 0) {
  to_add <- data.frame(
    Husband = missing$Father,
    Wife = missing$Mother,
    Marital.Status = "Co-Parents")
  
  part <- rbind(part, to_add)
}


## need to include the inverse of above to also get wife-->husband pairs
part <- data.frame(i = c(part$Husband, part$Wife), 
                    j = c(part$Wife, part$Husband), 
                    status = rep(part$Marital.Status, 2))

## check if any duplicates
# table(duplicated(paste(part$i, part$j)))
# see <- subset(part, duplicated(paste(part$i, part$j)) == TRUE)

## if so, need to decide which to retain!!
part <- subset(part, duplicated(paste(part$i, part$j)) == FALSE)

# table(duplicated(part$i))

# see <- subset(part, duplicated(part$i) == TRUE)
# multiple <- see$i

part$j_name <- indiv$firstname[match(part$j, indiv$IndivID)]

df <- part %>%
  group_by(i) %>%
  summarize(
    spouse_ids = paste(j, collapse = ", "), 
    spouse_names = paste(j_name, collapse = ", "), .groups = "drop"
  )


## Could remove cases of widowed marriages
#part2 <- part[-which(part$i %in% multiple & part$status == "widowed"), ]

indiv$spouse_id <- df$spouse_ids[match(indiv$IndivID, df$i)]
indiv$spousesname <- df$spouse_names[match(indiv$IndivID, df$i)]
indiv$spousesname[is.na(indiv$spousesname) == TRUE] <- ""

indiv$fathersname <- indiv$firstname[match(indiv$FatherID, indiv$IndivID)]
indiv$mothersname <- indiv$firstname[match(indiv$MotherID, indiv$IndivID)]

## now finally removing deceased people, once they've been able to populate other variables
indiv <- subset(indiv, !indiv$IndivID %in% deceased)

write.csv(indiv, "up_indiv_for_fuzz.csv", row.names = FALSE)
